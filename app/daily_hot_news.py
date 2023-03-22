import json
from datetime import date
import feedparser
import html2text

with open("app/data/hot_news_rss.json", "r") as f:
    rss_urls = json.load(f)

TODAY = today = date.today()
MAX_DESCRIPTION_LENGTH = 140
MAX_POSTS = 3


def cut_string(text):
    words = text.split()
    new_text = ""
    count = 0
    for word in words:
        if len(new_text + word) > MAX_DESCRIPTION_LENGTH:
            break
        new_text += word + " "
        count += 1

    return new_text.strip() + '...'

def get_text_from_html(html):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = True
    text_maker.ignore_tables = False
    text_maker.ignore_images = True
    return text_maker.handle(html)

def get_post_urls_with_title(rss_url):
    feed = feedparser.parse(rss_url)
    updated_posts = []
    
    for entry in feed.entries:
        published_time = entry.published_parsed if 'published_parsed' in entry else None
        # published_date = date(published_time.tm_year,
        #                       published_time.tm_mon, published_time.tm_mday)
        updated_post = {}
        updated_post['title'] = entry.title
        updated_post['summary'] = cut_string(get_text_from_html(entry.summary))
        updated_post['url'] = entry.link
        updated_post['publish_date'] = published_time
        updated_posts.append(updated_post)
        if len(updated_posts) >= MAX_POSTS:
            break
        
    return updated_posts

def build_slack_blocks(title, news):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{title} # {TODAY.strftime('%Y-%m-%d')}"
            }
        }]
    for news_item in news:
        blocks.extend([{
            "type": "section",
            "text": {
				"text": f"*{news_item['title']}*",
				"type": "mrkdwn"
			},
        },{
            "type": "section",
            "text": {
				"text": f"{news_item['summary']}",
				"type": "plain_text"
			},
        },{
            "type": "section",
            "text": {
				"text": f"原文链接：<{news_item['url']}>",
				"type": "mrkdwn"
			},
        },{
            "type": "divider"
        }])
    return blocks

def build_hot_news_blocks(news_key):
    rss = rss_urls[news_key]['rss']['hot']
    hot_news = get_post_urls_with_title(rss['url'])
    hot_news_blocks = build_slack_blocks(
        rss['name'], hot_news)
    return hot_news_blocks

def build_zhihu_hot_news_blocks():
    return build_hot_news_blocks('zhihu')

def build_v2ex_hot_news_blocks():
    return build_hot_news_blocks('v2ex')

def build_1point3acres_hot_news_blocks():
    return build_hot_news_blocks('1point3acres')

def build_reddit_news_hot_news_blocks():
    return build_hot_news_blocks('reddit-news')

def build_hackernews_news_hot_news_blocks():
    return build_hot_news_blocks('hackernews')

def build_producthunt_news_hot_news_blocks():
    return build_hot_news_blocks('producthunt')

def build_xueqiu_news_hot_news_blocks():
    return build_hot_news_blocks('xueqiu')

def build_jisilu_news_hot_news_blocks():
    return build_hot_news_blocks('jisilu')
