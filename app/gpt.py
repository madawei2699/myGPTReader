
import os
import logging
import hashlib
import openai
from llama_index import GPTSimpleVectorIndex, LLMPredictor, RssReader
from llama_index.prompts.prompts import QuestionAnswerPrompt
from llama_index.readers.schema.base import Document
from langchain.chat_models import ChatOpenAI

from app.fetch_web_post import get_urls, scrape_website, scrape_website_by_phantomjscloud

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo"))

index_cache_web_dir = '/tmp/myGPTReader/cache_web/'

if not os.path.exists(index_cache_web_dir):
    os.makedirs(index_cache_web_dir)

def get_unique_md5(urls):
    urls_str = ''.join(sorted(urls))
    hashed_str = hashlib.md5(urls_str.encode('utf-8')).hexdigest()
    return hashed_str

def format_dialog_messages(messages):
    return "\n".join(messages)

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

def get_answer_from_chatGPT(messages):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use chatGPT to answer!')
    logging.info(dialog_messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": dialog_messages}]
    )
    logging.info(completion.usage)
    return completion.choices[0].message.content

QUESTION_ANSWER_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "{query_str}\n"
)
QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL)

def get_index_from_web_cache(name):
    if not os.path.exists(index_cache_web_dir + name):
        return None
    index = GPTSimpleVectorIndex.load_from_disk(index_cache_web_dir + name)
    logging.info(f"=====> Get index from cache: {index_cache_web_dir + name}")
    return index

def get_answer_from_llama_web(messages, urls):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use llama with chatGPT to answer!')
    logging.info(dialog_messages)
    combained_urls = get_urls(urls)
    logging.info(combained_urls)
    index_file_name = get_unique_md5(urls)
    index = get_index_from_web_cache(index_file_name)
    if index is None:
        logging.info(f"=====> Build index from web!")
        documents = get_documents_from_urls(combained_urls)
        logging.info(documents)
        index = GPTSimpleVectorIndex(documents)
        logging.info(f"=====> Save index to disk path: {index_cache_web_dir + index_file_name}")
        index.save_to_disk(index_cache_web_dir + index_file_name)
    return index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)
