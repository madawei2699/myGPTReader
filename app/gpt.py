
import os
import hashlib
import openai
from llama_index import GPTChromaIndex, LLMPredictor, RssReader
from llama_index.prompts.prompts import QuestionAnswerPrompt
from llama_index import LangchainEmbedding
from llama_index.readers.schema.base import Document
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from chromadb.config import Settings
import chromadb

from app.fetch_web_post import get_urls, scrape_website, scrape_website_by_phantomjscloud

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

chroma_client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="/data/myGPTReader/chroma_db",
))

embed_model = LangchainEmbedding(HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))

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

def get_answer_from_chatGPT(messages, logger):
    dialog_messages = format_dialog_messages(messages)
    logger.info('=====> Use chatGPT to answer!')
    logger.info(dialog_messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": dialog_messages}]
    )
    logger.info(completion.usage)
    return completion.choices[0].message.content

QUESTION_ANSWER_PROMPT_TMPL = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "{query_str}\n"
)
QUESTION_ANSWER_PROMPT = QuestionAnswerPrompt(QUESTION_ANSWER_PROMPT_TMPL)

def get_answer_from_llama_web(messages, urls, logger):
    dialog_messages = format_dialog_messages(messages)
    logger.info('=====> Use llama with chatGPT to answer!')
    logger.info(dialog_messages)
    combained_urls = get_urls(urls)
    logger.info(combained_urls)
    documents = get_documents_from_urls(combained_urls)
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo"))
    logger.info(documents)
    chroma_collection = chroma_client.get_or_create_collection(get_unique_md5(urls))
    index = GPTChromaIndex(documents, chroma_collection=chroma_collection, embed_model=embed_model)
    return index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)