#!/usr/bin/env python3.8
import hashlib
import re
import logging
class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)
    
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