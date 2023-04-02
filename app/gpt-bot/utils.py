#!/usr/bin/env python3.8
import hashlib
import re
import logging
import os
import io
from pydub import AudioSegment

whitelist_file = "data//vip_whitelist.txt"
MAX_THREAD_MESSAGE_HISTORY = 10
class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)

# 提取普通 text 的文本和链接
def extract_text_and_links_from_content(input_dict):
    input_str = input_dict.get("text", "")
    # 匹配文本中的链接
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url_match = url_pattern.search(input_str)
    
    if url_match:
        # 提取链接
        link = url_match.group(0)
        
        # 删除链接，提取文案
        text = url_pattern.sub('', input_str).strip()

        return {"text": [text], "link": [link]}
    else:
        return {"text": [input_str], "link": []}

# 提取话题群类型 post 的文本和链接
def extract_post_text_and_links_from_content(input_dict):
    content_list = input_dict.get('content', '[]')

    extracted_text = []
    extracted_links = []
    
    for item in content_list:
        for element in item:
            if element.get('tag') == 'text':
                extracted_text.append(element.get('text'))
            elif element.get('tag') == 'a':
                extracted_links.append(element.get('href'))
    
    return {"text": extracted_text,"link": extracted_links}

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_youtube_video_id(url):
    if url is None:
        return None
    if 'youtube.com' in url:
        return url.split('v=')[-1]
    if 'youtu.be' in url:
        return url.split('/')[-1]
    return None

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

def get_file_extension(filename):
    _, file_extension = os.path.splitext(filename)
    return file_extension[1:]  # 使用字符串切片去掉点

def setup_logger(name, log_level=logging.INFO):
    # 创建一个日志器（logger）
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # 创建一个处理器（handler）以将日志消息输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 定义一个包含时间戳的日志格式
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 将日志格式应用于处理器
    console_handler.setFormatter(log_format)

    # 将处理器添加到日志器
    logger.addHandler(console_handler)

    return logger

# 根据二进制文件获取音频格式
def identify_audio_format(binary_data):
    # Check magic numbers
    if binary_data.startswith(b'\xFF\xF1') or binary_data.startswith(b'\xFF\xF9'):
        return 'mp3'
    elif binary_data.startswith(b'RIFF') and binary_data[8:12] == b'WAVE':
        return 'wav'
    elif binary_data.startswith(b'OggS'):
        return 'ogg'
    elif binary_data.startswith(b'fLaC'):
        return 'flac'
    elif binary_data.startswith(b'\x00\x00\x00\x1CftypM4A'):
        return 'm4a'
    elif binary_data.startswith(b'\x1aE\xdf\xa3'):
        return 'webm'
    else:
        return 'ogg'
    
# 音频格式转化
def convert_ogg_to_mp3_binary(ogg_binary_data, audio_format):
    supported_formats = ['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg']
    # If the audio format is already supported, return the original data
    if audio_format.lower() in supported_formats:
        return ogg_binary_data
    # Create a BytesIO object from the binary data
    ogg_buffer = io.BytesIO(ogg_binary_data)

    # Read OGG data from the BytesIO object
    ogg_audio = AudioSegment.from_ogg(ogg_buffer)

    # Create a BytesIO object for the MP3 data
    mp3_buffer = io.BytesIO()

    # Export the audio as MP3 to the BytesIO object
    ogg_audio.export(mp3_buffer, format="mp3")

    # Return the binary MP3 data
    return mp3_buffer.getvalue()

def is_authorized(user_id: str) -> bool:
    with open(whitelist_file, "r") as f:
        return user_id in f.read().splitlines()
    
# 更新文本、链接和文件，用户建立问题以及向量索引
def update_thread_history(thread_message_history, thread_id, message_str=None, urls=None, file=None):
    if urls is not None:
        thread_message_history[thread_id]['context_urls'].update(urls)
    if message_str is not None:
        if thread_id in thread_message_history:
            dialog_texts = thread_message_history[thread_id]['dialog_texts']
            dialog_texts = dialog_texts + message_str
            if len(dialog_texts) > MAX_THREAD_MESSAGE_HISTORY:
                dialog_texts = dialog_texts[-MAX_THREAD_MESSAGE_HISTORY:]
            thread_message_history[thread_id]['dialog_texts'] = dialog_texts
        else:
            thread_message_history[thread_id]['dialog_texts'] = message_str
    if file is not None:
        thread_message_history[thread_id]['file'] = file

def dialog_context_keep_latest(dialog_texts, max_length=1):
    if len(dialog_texts) > max_length:
        dialog_texts = dialog_texts[-max_length:]
    return dialog_texts