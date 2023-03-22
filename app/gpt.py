
import os
import logging
import hashlib
import random
import uuid
import openai
from langdetect import detect
from llama_index import GPTSimpleVectorIndex, LLMPredictor, RssReader, SimpleDirectoryReader
from llama_index.prompts.prompts import QuestionAnswerPrompt
from llama_index.readers.schema.base import Document
from langchain.chat_models import ChatOpenAI
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason, CancellationReason, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from app.fetch_web_post import get_urls, scrape_website, scrape_website_by_phantomjscloud

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SPEECH_KEY = os.environ.get('SPEECH_KEY')
SPEECH_REGION = os.environ.get('SPEECH_REGION')
openai.api_key = OPENAI_API_KEY

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.2, model_name="gpt-3.5-turbo"))

index_cache_web_dir = '/tmp/myGPTReader/cache_web/'
index_cache_voice_dir = '/tmp/myGPTReader/voice/'
index_cache_file_dir = '/data/myGPTReader/file/'

if not os.path.exists(index_cache_web_dir):
    os.makedirs(index_cache_web_dir)

if not os.path.exists(index_cache_voice_dir):
    os.makedirs(index_cache_voice_dir)

if not os.path.exists(index_cache_file_dir):
    os.makedirs(index_cache_file_dir)


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
    logging.info(
        f"=====> Get index from web cache: {index_cache_web_dir + name}")
    return index


def get_index_from_file_cache(name):
    if not os.path.exists(index_cache_file_dir + name):
        return None
    index = GPTSimpleVectorIndex.load_from_disk(index_cache_file_dir + name)
    logging.info(
        f"=====> Get index from file cache: {index_cache_file_dir + name}")
    return index


def get_answer_from_llama_web(messages, urls):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use llama web with chatGPT to answer!')
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
        logging.info(
            f"=====> Save index to disk path: {index_cache_web_dir + index_file_name}")
        index.save_to_disk(index_cache_web_dir + index_file_name)
    return index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)


def get_index_name_from_file(file: str):
    file_md5_with_extension = file.replace(index_cache_file_dir, '')
    file_md5 = file_md5_with_extension.split('.')[0]
    return file_md5 + '.json'


def get_answer_from_llama_file(messages, file):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use llama file with chatGPT to answer!')
    logging.info(dialog_messages)
    index_name = get_index_name_from_file(file)
    index = get_index_from_file_cache(index_name)
    if index is None:
        logging.info(f"=====> Build index from file!")
        documents = SimpleDirectoryReader(input_files=[file]).load_data()
        index = GPTSimpleVectorIndex(documents)
        logging.info(
            f"=====> Save index to disk path: {index_cache_file_dir + index_name}")
        index.save_to_disk(index_cache_file_dir + index_name)
    return index.query(dialog_messages, llm_predictor=llm_predictor, text_qa_template=QUESTION_ANSWER_PROMPT)


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
    lang_code = detect(text)
    text = remove_prompt_from_text(text)
    try:
        if voice_name is None:
            voice_name = random.choice(lang_code_voice_map[lang_code.split('-')[0]])
    except Exception as e:
        logging.warning(f"Error: {e}. Using default voice.")
        voice_name = random.choice(lang_code_voice_map['en'])
    ssml = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="zh-CN">'
    ssml += f'<voice name="{voice_name}">{text}</voice>'
    ssml += '</speak>'

    return ssml

def get_voice_file_from_text(text, voice_name=None):
    speech_config = SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.set_speech_synthesis_output_format(
        SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    speech_config.speech_synthesis_language = "zh-CN"
    file_name = f"{index_cache_voice_dir}{uuid.uuid4()}.mp3"
    file_config = AudioOutputConfig(filename=file_name)
    synthesizer = SpeechSynthesizer(
        speech_config=speech_config, audio_config=file_config)
    ssml = convert_to_ssml(text, voice_name)
    result = synthesizer.speak_ssml_async(ssml).get()
    if result.reason == ResultReason.SynthesizingAudioCompleted:
        logging.info("Speech synthesized for text [{}], and the audio was saved to [{}]".format(
            text, file_name))
    elif result.reason == ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        logging.info("Speech synthesis canceled: {}".format(
            cancellation_details.reason))
        if cancellation_details.reason == CancellationReason.Error:
            logging.error("Error details: {}".format(
                cancellation_details.error_details))
    return file_name
