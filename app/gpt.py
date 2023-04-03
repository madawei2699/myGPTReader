
import os
import hashlib
import random
import openai
from pathlib import Path
from langdetect import detect
from llama_index import GPTSimpleVectorIndex, LLMPredictor, SimpleDirectoryReader
from llama_index.prompts.prompts import QuestionAnswerPrompt
from llama_index.readers.schema.base import Document
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from utils import setup_logger

from fetch_web_post import get_urls, get_youtube_transcript, scrape_website
from utils import get_youtube_video_id
# load env parameters form file named .env
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_KEY_SECOND = os.getenv('OPENAI_API_KEY_SECOND')
logging = setup_logger('my_gpt_reader_gpt')
# SPEECH_KEY = os.environ.get('SPEECH_KEY')
# SPEECH_REGION = os.environ.get('SPEECH_REGION')
# 将 API 密钥放入列表中
api_keys = [OPENAI_API_KEY, OPENAI_API_KEY_SECOND]
# 随机选择一个 API 密钥
chosen_api_key = random.choice(api_keys)
# 将选定的 API 密钥分配给 openai.api_key
openai.api_key = chosen_api_key

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.2, model_name="gpt-3.5-turbo"))
# the "mock" llm predictor is our token counter
# mock_llm_predictor = MockLLMPredictor(max_tokens=256)÷=

index_cache_web_dir = Path('/tmp/myGPTReader/cache_web/')
index_cache_voice_dir = Path('/tmp/myGPTReader/voice/')
home_dir = os.path.expanduser("~")
index_cache_file_dir = Path(home_dir, "myGPTReader", "file")

if not index_cache_web_dir.is_dir():
    index_cache_web_dir.mkdir(parents=True, exist_ok=True)

if not index_cache_voice_dir.is_dir():
    index_cache_voice_dir.mkdir(parents=True, exist_ok=True)

if not index_cache_file_dir.is_dir():
    index_cache_file_dir.mkdir(parents=True, exist_ok=True)

def get_unique_md5(urls):
    urls_str = ''.join(sorted(urls))
    hashed_str = hashlib.md5(urls_str.encode('utf-8')).hexdigest()
    return hashed_str

def format_dialog_messages(messages):
    return "\n".join(messages)

def get_document_from_youtube_id(video_id):
    if video_id is None:
        return None
    transcript = get_youtube_transcript(video_id)
    if transcript is None:
        return None
    return Document(transcript)

def get_documents_from_urls(urls):
    documents = []
    for url in urls['page_urls']:
        document = Document(scrape_website(url))
        documents.append(document)
    if len(urls['youtube_urls']) > 0:
        for url in urls['youtube_urls']:
            video_id = get_youtube_video_id(url)
            document = get_document_from_youtube_id(video_id)
            if (document is not None):
                documents.append(document)
            else:
                documents.append(Document(f"Can't get transcript from youtube video: {url}"))
    return documents

def get_answer_from_chatGPT(messages):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use chatGPT to answer!')
    logging.info(dialog_messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": dialog_messages}]
    )
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
    web_cache_file = index_cache_web_dir / name
    if not web_cache_file.is_file():
        return None
    index = GPTSimpleVectorIndex.load_from_disk(web_cache_file)
    logging.info(
        f"=====> Get index from web cache: {web_cache_file}")
    return index


def get_index_from_file_cache(name):
    file_cache_file = index_cache_file_dir / name
    if not file_cache_file.is_file():
        return None
    index = GPTSimpleVectorIndex.load_from_disk(file_cache_file)
    logging.info(
        f"=====> Get index from file cache: {file_cache_file}")
    return index

def get_answer_from_llama_web(messages, urls):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use llama web with chatGPT to answer!')
    # logging.info(dialog_messages)
    combained_urls = get_urls(urls)
    logging.info(combained_urls)
    index_file_name = get_unique_md5(urls)
    index = get_index_from_web_cache(index_file_name)
    if index is None:
        logging.info(f"=====> Build index from web!")
        documents = get_documents_from_urls(combained_urls)
        index = GPTSimpleVectorIndex(documents)
        logging.info(
            f"=====> Save index to disk path: {index_cache_web_dir / index_file_name}")
        
        index.save_to_disk(index_cache_web_dir / index_file_name)
    answer = index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)
    logging.info(
            f"=====> get_answer_from_llama_web GPTSimpleVectorIndex query tokens: {llm_predictor.last_token_usage}")
    return answer
def get_index_name_from_file(file: str):
    file_md5_with_extension = str(Path(file).relative_to(index_cache_file_dir).name)
    file_md5 = file_md5_with_extension.split('.')[0]
    return file_md5 + '.json'

def get_answer_from_llama_file(messages, file):
    dialog_messages = format_dialog_messages(messages)
    logging.info(f'=====> Use llama file with chatGPT to answer! => {dialog_messages == ""}')
    logging.info(dialog_messages)
    index_name = get_index_name_from_file(file)
    index = get_index_from_file_cache(index_name)
    if index is None:
        logging.info(f"=====> Build index from file!")
        documents = SimpleDirectoryReader(input_files=[file]).load_data()
        index = GPTSimpleVectorIndex(documents)
        logging.info(
            f"=====> Save index to disk path: {index_cache_file_dir / index_name}, get_answer_from_llama_file documents last_token_usage is {llm_predictor.last_token_usage}")
        index.save_to_disk(index_cache_file_dir / index_name)
    if dialog_messages == '':
        logging.info(f"=====> dialog_messages is empty, just build file index!")
        return "没有输入内容，已经根据文件建立索引，请在此消息后回复对于文件的问题"
    answer = index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)
    return answer

def get_text_from_whisper(voice_file_path):
    with open(voice_file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript.text

def remove_prompt_from_text(text):
    return text.replace('AI:', '').strip()

lang_code_voice_map = {
    'zh': ['zh-CN-XiaoxiaoNeural', 'zh-CN-XiaohanNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunyangNeural'],
    'en': ['en-US-JennyNeural', 'en-US-RogerNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-AU-AnnetteNeural', 'en-AU-CarlyNeural', 'en-GB-AbbiNeural', 'en-GB-AlfieNeural'],
    'ja': ['ja-JP-AoiNeural', 'ja-JP-DaichiNeural'],
    'de': ['de-DE-AmalaNeural', 'de-DE-BerndNeural'],
}

def convert_to_ssml(text, voice_name=None):
    try:
        logging.info("=====> Convert text to ssml!")
        logging.info(text)
        text = remove_prompt_from_text(text)
        lang_code = detect(text)
        if voice_name is None:
            voice_name = random.choice(lang_code_voice_map[lang_code.split('-')[0]])
    except Exception as e:
        logging.warning(f"Error: {e}. Using default voice.")
        voice_name = random.choice(lang_code_voice_map['zh'])
    ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">'
    ssml += f'<voice name="{voice_name}">{text}</voice>'
    ssml += '</speak>'

    return ssml
