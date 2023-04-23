import hashlib
import logging
from langdetect import detect

def md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def get_youtube_video_id(url):
    if url is None:
        return None
    if 'youtube.com/watch?v=' in url:
        return url.split('v=')[-1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com/embed/' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com/v/' in url:
        return url.split('/')[-1].split('?')[0]
    elif 'youtube.com/live/' in url:
        if '?v=' in url:
            return url.split('?v=')[-1].split('&')[0]
        else:
            return url.split('/')[-1].split('?')[0]
    return None

def get_language_code(text):
    try:
        return detect(text).split('-')[0]
    except Exception as e:
        logging.error(e)
        return 'zh'
