
import os
import logging
import hashlib
import random
import uuid
import openai
from pathlib import Path
from llama_index import ServiceContext, GPTVectorStoreIndex, LLMPredictor, RssReader, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.readers.schema.base import Document
from langchain.chat_models import ChatOpenAI
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason, CancellationReason, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

from app.fetch_web_post import get_urls, get_youtube_transcript, scrape_website, scrape_website_by_phantomjscloud
from app.prompt import get_prompt_template
from app.util import get_language_code, get_youtube_video_id

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
SPEECH_KEY = os.environ.get('SPEECH_KEY')
SPEECH_REGION = os.environ.get('SPEECH_REGION')
openai.api_key = OPENAI_API_KEY

index_cache_web_dir = Path('/tmp/myGPTReader/cache_web/')
index_cache_file_dir = Path('/data/myGPTReader/file/')
index_cache_voice_dir = Path('/tmp/myGPTReader/voice/')

if not index_cache_web_dir.is_dir():
    index_cache_web_dir.mkdir(parents=True, exist_ok=True)

if not index_cache_voice_dir.is_dir():
    index_cache_voice_dir.mkdir(parents=True, exist_ok=True)

if not index_cache_file_dir.is_dir():
    index_cache_file_dir.mkdir(parents=True, exist_ok=True)

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0, model_name="gpt-3.5-turbo"))

service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

web_storage_context = StorageContext.from_defaults()
file_storage_context = StorageContext.from_defaults()

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

def remove_prompt_from_text(text):
    return text.replace('chatGPT:', '').strip()

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
    if len(urls['youtube_urls']) > 0:
        for url in urls['youtube_urls']:
            video_id = get_youtube_video_id(url)
            document = get_document_from_youtube_id(video_id)
            if (document is not None):
                documents.append(document)
            else:
                documents.append(Document(f"Can't get transcript from youtube video: {url}"))
    return documents

def get_index_from_web_cache(name):
    try:
        index = load_index_from_storage(web_storage_context, index_id=name)
    except Exception as e:
        logging.error(e)
        return None
    return index

def get_index_from_file_cache(name):
    try:
        index = load_index_from_storage(file_storage_context, index_id=name)
    except Exception as e:
        logging.error(e)
        return None
    return index

def get_index_name_from_file(file: str):
    file_md5_with_extension = str(Path(file).relative_to(index_cache_file_dir).name)
    file_md5 = file_md5_with_extension.split('.')[0]
    return file_md5

def get_answer_from_chatGPT(messages):
    dialog_messages = format_dialog_messages(messages)
    logging.info('=====> Use chatGPT to answer!')
    logging.info(dialog_messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": dialog_messages}]
    )
    logging.info(completion.usage)
    total_tokens = completion.usage.total_tokens
    return completion.choices[0].message.content, total_tokens, None

def get_answer_from_llama_web(messages, urls):
    dialog_messages = format_dialog_messages(messages)
    lang_code = get_language_code(remove_prompt_from_text(messages[-1]))
    combained_urls = get_urls(urls)
    logging.info(combained_urls)
    index_file_name = get_unique_md5(urls)
    index = get_index_from_web_cache(index_file_name)
    if index is None:
        logging.info(f"=====> Build index from web!")
        documents = get_documents_from_urls(combained_urls)
        logging.info(documents)
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        index.set_index_id(index_file_name)
        index.storage_context.persist()
        logging.info(
            f"=====> Save index to disk path: {index_cache_web_dir / index_file_name}")
    prompt = get_prompt_template(lang_code)
    logging.info('=====> Use llama web with chatGPT to answer!')
    logging.info('=====> dialog_messages')
    logging.info(dialog_messages)
    logging.info('=====> text_qa_template')
    logging.info(prompt.prompt)
    answer = index.as_query_engine(text_qa_template=prompt).query(dialog_messages)
    total_llm_model_tokens = llm_predictor.last_token_usage
    total_embedding_model_tokens = service_context.embed_model.last_token_usage
    return answer, total_llm_model_tokens, total_embedding_model_tokens

def get_answer_from_llama_file(messages, file):
    dialog_messages = format_dialog_messages(messages)
    lang_code = get_language_code(remove_prompt_from_text(messages[-1]))
    index_name = get_index_name_from_file(file)
    index = get_index_from_file_cache(index_name)
    if index is None:
        logging.info(f"=====> Build index from file!")
        documents = SimpleDirectoryReader(input_files=[file]).load_data()
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        index.set_index_id(index_name)
        index.storage_context.persist()
        logging.info(
            f"=====> Save index to disk path: {index_cache_file_dir / index_name}")
    prompt = get_prompt_template(lang_code)
    logging.info('=====> Use llama file with chatGPT to answer!')
    logging.info('=====> dialog_messages')
    logging.info(dialog_messages)
    logging.info('=====> text_qa_template')
    logging.info(prompt)
    answer = answer = index.as_query_engine(text_qa_template=prompt).query(dialog_messages)
    total_llm_model_tokens = llm_predictor.last_token_usage
    total_embedding_model_tokens = service_context.embed_model.last_token_usage
    return answer, total_llm_model_tokens, total_embedding_model_tokens

def get_text_from_whisper(voice_file_path):
    with open(voice_file_path, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript.text

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
        lang_code = get_language_code(text)
        if voice_name is None:
            voice_name = random.choice(lang_code_voice_map[lang_code])
    except Exception as e:
        logging.warning(f"Error: {e}. Using default voice.")
        voice_name = random.choice(lang_code_voice_map['zh'])
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
