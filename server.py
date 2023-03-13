from urllib.parse import urlparse
from flask import Flask, request
import re
import os
import openai
import feedparser
import validators
import html2text
import json
from slack_bolt import App
import requests
from slack_bolt.adapter.flask import SlackRequestHandler
from llama_index import GPTSimpleVectorIndex, LLMPredictor, RssReader
from llama_index.readers.schema.base import Document
from llama_index.prompts.prompts import QuestionAnswerPrompt
from langchain.chat_models import ChatOpenAI
import concurrent.futures

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

CF_ACCESS_CLIENT_ID = os.environ.get('CF_ACCESS_CLIENT_ID')
CF_ACCESS_CLIENT_SECRET = os.environ.get('CF_ACCESS_CLIENT_SECRET')

PHANTOMJSCLOUD_API_KEY = os.environ.get('PHANTOMJSCLOUD_API_KEY')
PHANTOMJSCLOUD_WEBSITES = ['https://twitter.com/', 'https://t.co/', 'https://medium.com/', 'https://app.mailbrew.com/', 'https://us12.campaign-archive.com', 'https://news.ycombinator.com', 'https://www.bloomberg.com']

slack_app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
slack_handler = SlackRequestHandler(slack_app)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return slack_handler.handle(request)

def insert_space(text):

    # Handling the case between English words and Chinese characters
    text = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1 \2', text)

    # Handling the situation between numbers and Chinese
    text = re.sub(r'(\d)([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])(\d)', r'\1 \2', text)

    # handling the special characters
    text = re.sub(r'([\W_])([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])([\W_])', r'\1 \2', text)

    text = text.replace('  ', ' ')

    return text

def extract_urls_from_event(event):
    urls = set()
    for block in event['blocks']:
        for element in block['elements']:
            for e in element['elements']:
                if e['type'] == 'link':
                    url = urlparse(e['url']).geturl()
                    urls.add(url)
    return list(urls)

def check_if_need_use_phantomjscloud(url):
    return any(url.startswith(site) for site in PHANTOMJSCLOUD_WEBSITES)

def get_urls(urls):
    rss_urls = []
    page_urls = []
    phantomjscloud_urls = []
    for url in urls:
        if validators.url(url):
            feed = feedparser.parse(url)
            if feed.version:
                rss_urls.append(url)
            elif check_if_need_use_phantomjscloud(url):
                phantomjscloud_urls.append(url)
            else:
                page_urls.append(url)
    return {'rss_urls': rss_urls, 'page_urls': page_urls, 'phantomjscloud_urls': phantomjscloud_urls}

def format_text(text):
    text_without_html_tag = html2text.html2text(text)
    fix_chinese_split_chunk_size_error = text_without_html_tag.replace('，', '， ')
    return fix_chinese_split_chunk_size_error

def scrape_website(url: str) -> str:
    endpoint_url = f"https://web-scraper.i365.tech/?url={url}&selector=div"
    headers = {
        'CF-Access-Client-Id': CF_ACCESS_CLIENT_ID,
        'CF-Access-Client-Secret': CF_ACCESS_CLIENT_SECRET,
    }
    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        try:
            json_response = response.json()
            tag_array = json_response['result']['div']
            text = ''.join(tag_array)
            return format_text(text)
        except:
            return "Error: Unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.reason}"
    
def scrape_website_by_phantomjscloud(url: str) -> str:
    endpoint_url = f"https://PhantomJsCloud.com/api/browser/v2/{PHANTOMJSCLOUD_API_KEY}/"
    data ={
        "url": url,
        "renderType" : "plainText",
        "requestSettings":{
            "doneWhen":[
                {
                    "event": "domReady"
                },
            ],
        }
    }
    response = requests.post(endpoint_url, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.content.decode('utf-8')
        except:
            return "Error: Unable to fetch content"
    else:
        return f"Error: {response.status_code} - {response.reason}"
    
def get_documents_from_urls(urls):
    documents = []
    for url in urls['page_urls']:
        document = Document(scrape_website(url))
        documents.append(document)
    if len(urls['rss_urls']) > 0:
        rss_documents = RssReader().load_data(urls['rss_urls'])
        documents = documents + rss_documents
    if len(urls['phantomjscloud_urls']) > 0:
        for url in urls['phantomjscloud_urls']:
            document = Document(scrape_website_by_phantomjscloud(url))
            documents.append(document)
    return documents

def get_answer_from_chatGPT(message, logger):
    logger.info('=====> Use chatGPT to answer!')
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    logger.info(completion.usage)
    return completion.choices[0].message.content

QUESTION_ANSWER_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Given the context information and not prior knowledge, "
    "Please answer this question line by line using the same language as the question: {query_str}\n"
)
QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL)

def get_answer_from_llama_web(message, urls, logger):
    logger.info('=====> Use llama with chatGPT to answer!')
    combained_urls = get_urls(urls)
    logger.info(combained_urls)
    documents = get_documents_from_urls(combained_urls)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    logger.info(documents)
    index = GPTSimpleVectorIndex(documents, text_qa_template=QUESTION_ANSWER_PROMPT)
    return index.query(message, llm_predictor=llm_predictor)

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    logger.info(event)
    user = event["user"]
    text = event["text"]
    thread_ts = event["ts"]
    user_message = text.replace('<@U04TCNR9MNF>', '')

    message_normalized = insert_space(user_message)
    urls = extract_urls_from_event(event)

    if len(urls) > 0:
        future = executor.submit(get_answer_from_llama_web, message_normalized, urls, logger)
    else:
        future = executor.submit(get_answer_from_chatGPT, message_normalized, logger)

    try:
        gpt_response = future.result(timeout=300)
        logger.info(gpt_response)
        say(f'<@{user}>, {gpt_response}', thread_ts=thread_ts)
    except concurrent.futures.TimeoutError:
        future.cancel()
        err_msg = 'Task timedout(5m) and was canceled.'
        logger.warning(err_msg)
        say(f'<@{user}>, {err_msg}', thread_ts=thread_ts)

if __name__ == '__main__':
    app.run(debug=True)
