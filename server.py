from urllib.parse import urlparse
from flask import Flask, request
import re
import os
import openai
from slack_bolt import App
import requests
from slack_bolt.adapter.flask import SlackRequestHandler
from llama_index import GPTListIndex, LLMPredictor
from llama_index.prompts.default_prompts import DEFAULT_REFINE_PROMPT
from llama_index.readers.schema.base import Document
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

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

def scrape_website(url: str) -> str:
    endpoint_url = f"https://web.scraper.workers.dev/?url={url}&selector=body"
    response = requests.get(endpoint_url)
    if response.status_code == 200:
        try:
            json_response = response.json()
            body_array = json_response['result']['body']
            body_str = ''.join(body_array)
            return body_str
        except:
            return "Error: Unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.reason}"
    
def get_documents_from_urls(urls):
    documents = []
    for url in urls:
        document = Document(scrape_website(url))
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

def get_answer_from_llama_web(message, urls, logger):
    logger.info('=====> Use llama with chatGPT to answer!')
    logger.info(urls)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    documents = get_documents_from_urls(urls)
    logger.info(documents)
    index = GPTListIndex(documents)
    return index.query(message, llm_predictor=llm_predictor,
                       refine_template=DEFAULT_REFINE_PROMPT)

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    logger.info(event)
    user = event["user"]
    text = event["text"]
    user_message = text.replace('<@U04TCNR9MNF>', '')

    message_normalized = insert_space(user_message)
    urls = extract_urls_from_event(event)

    if len(urls) > 0:
        gpt_response = get_answer_from_llama_web(message_normalized, urls, logger)
    else:
        gpt_response = get_answer_from_chatGPT(message_normalized, logger)

    logger.info(gpt_response)

    say(f'<@{user}>, {gpt_response}')

if __name__ == '__main__':
    app.run(debug=True)
