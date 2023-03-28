#!/usr/bin/env python3.8
import hashlib
import re
class Obj(dict):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Obj(b) if isinstance(b, dict) else b)


def dict_2_obj(d: dict):
    return Obj(d)

def extract_link_and_text(input_dict):
    input_str = input_dict.get("text", "")
    # 匹配文本中的链接
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    url_match = url_pattern.search(input_str)
    
    if url_match:
        # 提取链接
        link = url_match.group(0)
        
        # 删除链接，提取文案
        text = url_pattern.sub('', input_str).strip()

        return {"text": text, "link": [link]}
    else:
        return {"text": input_str, "link": None}

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