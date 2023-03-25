import hashlib

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