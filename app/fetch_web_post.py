import os
import json
import html2text
import requests
import feedparser
import validators
import fnmatch

CF_ACCESS_CLIENT_ID = os.environ.get('CF_ACCESS_CLIENT_ID')
CF_ACCESS_CLIENT_SECRET = os.environ.get('CF_ACCESS_CLIENT_SECRET')

PHANTOMJSCLOUD_API_KEY = os.environ.get('PHANTOMJSCLOUD_API_KEY')
PHANTOMJSCLOUD_WEBSITES = ['https://twitter.com/', 'https://t.co/', 'https://medium.com/', 'https://app.mailbrew.com/', 'https://us12.campaign-archive.com', 'https://news.ycombinator.com', 'https://www.bloomberg.com', 'https://*.substack.com/*', 'https://*.1point3acres.com/*', 'https://www.v2ex.com', 'https://www.producthunt.com', 'http://xueqiu.com', 'https://www.jisilu.cn']

def check_if_need_use_phantomjscloud(url):
    for site in PHANTOMJSCLOUD_WEBSITES:
        if fnmatch.fnmatch(url, site):
                return True
        elif url.startswith(site):
            return True
    return False

def get_urls(urls):
    rss_urls = []
    page_urls = []
    phantomjscloud_urls = []
    for url in urls:
        if validators.url(url):
            feed = feedparser.parse(url)
            if feed.version:
                rss_urls.append(url)
            elif check_if_need_use_phantomjscloud(url):
                phantomjscloud_urls.append(url)
            else:
                page_urls.append(url)
    return {'rss_urls': rss_urls, 'page_urls': page_urls, 'phantomjscloud_urls': phantomjscloud_urls}

def format_text(text):
    text_without_html_tag = html2text.html2text(text)
    fix_chinese_split_chunk_size_error = text_without_html_tag.replace('，', '， ')
    return fix_chinese_split_chunk_size_error

def scrape_website(url: str) -> str:
    endpoint_url = f"https://web-scraper.i365.tech/?url={url}&selector=div"
    headers = {
        'CF-Access-Client-Id': CF_ACCESS_CLIENT_ID,
        'CF-Access-Client-Secret': CF_ACCESS_CLIENT_SECRET,
    }
    response = requests.get(endpoint_url, headers=headers)
    if response.status_code == 200:
        try:
            json_response = response.json()
            tag_array = json_response['result']['div']
            text = ''.join(tag_array)
            return format_text(text)
        except:
            return "Error: Unable to parse JSON response"
    else:
        return f"Error: {response.status_code} - {response.reason}"
    
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
