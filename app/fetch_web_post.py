import logging
import os
import json
import html2text
import requests
import feedparser
import validators
import fnmatch
from youtube_transcript_api import YouTubeTranscriptApi
from scrapers import _parse_url_or_html
import grpc
import service_pb2_grpc

PHANTOMJSCLOUD_API_KEY = os.environ.get('PHANTOMJSCLOUD_API_KEY')
PHANTOMJSCLOUD_WEBSITES = ['https://twitter.com/', 'https://t.co/', 'https://medium.com/', 'https://app.mailbrew.com/', 'https://us12.campaign-archive.com', 'https://news.ycombinator.com', 'https://www.bloomberg.com', 'https://*.substack.com/*', 'https://*.1point3acres.com/*', 'https://www.v2ex.com', 'https://www.producthunt.com', 'http://xueqiu.com', 'https://www.jisilu.cn', 'https://www.163.com']

channel = grpc.insecure_channel("localhost:50051")
stub = service_pb2_grpc.MyServiceStub(channel)

def check_if_need_use_phantomjscloud(url):
    for site in PHANTOMJSCLOUD_WEBSITES:
        if fnmatch.fnmatch(url, site):
                return True
        elif url.startswith(site):
            return True
    return False

def check_if_youtube_url(url):
    return 'youtube.com' in url or 'youtu.be' in url

def get_urls(urls):
    rss_urls = []
    page_urls = []
    phantomjscloud_urls = []
    youtube_urls = []
    for url in urls:
        if validators.url(url):
            feed = feedparser.parse(url)
            if hasattr(feed, 'version') and feed.version:
                rss_urls.append(url)
            elif check_if_need_use_phantomjscloud(url):
                phantomjscloud_urls.append(url)
            elif check_if_youtube_url(url):
                youtube_urls.append(url)
            else:
                page_urls.append(url)
    return {'rss_urls': rss_urls, 'page_urls': page_urls, 'phantomjscloud_urls': phantomjscloud_urls, 'youtube_urls': youtube_urls}

def format_text(text):
    text_without_html_tag = html2text.html2text(text)
    fix_chinese_split_chunk_size_error = text_without_html_tag.replace('，', '， ')
    return fix_chinese_split_chunk_size_error

def scrape_website(url: str) -> str:
    result = _parse_url_or_html(url);
    try:
        text_content = html2text.html2text(result)
        print(f'result 成功=>{text_content}')
        return text_content
    except Exception as e:
        logging.warning(f"html2text.html2text error: {e}")
        return f"Error: {e}"
    
def scrape_website_by_phantomjscloud(url: str) -> str:
    endpoint_url = f"https://PhantomJsCloud.com/api/browser/v2/{PHANTOMJSCLOUD_API_KEY}/"
    data ={
        "url": url,
        "renderType" : "plainText",
        "requestSettings":{
            "doneWhen":[
                {
                    "event": "domReady"
                },
            ],
        }
    }
    response = requests.post(endpoint_url, data=json.dumps(data))
    if response.status_code == 200:
        try:
            return response.content.decode('utf-8')
        except:
            return "Error: Unable to fetch content"
    else:
        return f"Error: {response.status_code} - {response.reason}"
    
def get_youtube_transcript(video_id: str) -> str:
    try:
        srt = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for chunk in srt:
            transcript = transcript + chunk["text"] + "\n"
    except Exception as e:
        logging.warning(f"Error: {e} - {video_id}")
        transcript = None
    return transcript
