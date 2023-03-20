import re
import os
from urllib.parse import urlparse
from flask import Flask, request
from flask_apscheduler import APScheduler
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import concurrent.futures
from app.daily_hot_news import *
from app.gpt import get_answer_from_chatGPT, get_answer_from_llama_web
from app.slash_command import register_slack_slash_commands

class Config:
    SCHEDULER_API_ENABLED = True

executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

schedule_channel = "#daily-news"

app = Flask(__name__)

slack_app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
slack_handler = SlackRequestHandler(slack_app)

scheduler = APScheduler()
scheduler.api_enabled = True
scheduler.init_app(app)

def send_daily_news(client, news):
    for news_item in news:
        client.chat_postMessage(
            channel=schedule_channel,
            text="",
            blocks=news_item,
            reply_broadcast=True
        )

@scheduler.task('cron', id='daily_news_task', hour=1, minute=30)
def schedule_news():
   zhihu_news = build_zhihu_hot_news_blocks()
   v2ex_news = build_v2ex_hot_news_blocks()
   onepoint3acres_news = build_1point3acres_hot_news_blocks()
   reddit_news = build_reddit_news_hot_news_blocks()
   hackernews_news = build_hackernews_news_hot_news_blocks()
   producthunt_news = build_producthunt_news_hot_news_blocks()
   xueqiu_news = build_xueqiu_news_hot_news_blocks()
   jisilu_news = build_jisilu_news_hot_news_blocks()
   send_daily_news(slack_app.client, [zhihu_news, v2ex_news, onepoint3acres_news, reddit_news, hackernews_news, producthunt_news, xueqiu_news, jisilu_news])

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return slack_handler.handle(request)

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

thread_message_history = {}
MAX_THREAD_MESSAGE_HISTORY = 10

def update_thread_history(thread_ts, message_str, urls=None):
    if urls is not None:
        thread_message_history[thread_ts]['context_urls'].update(urls)
    if thread_ts in thread_message_history:
        dialog_texts = thread_message_history[thread_ts]['dialog_texts']
        dialog_texts.append(message_str)
        if len(dialog_texts) > MAX_THREAD_MESSAGE_HISTORY:
            dialog_texts = dialog_texts[-MAX_THREAD_MESSAGE_HISTORY:]
        thread_message_history[thread_ts]['dialog_texts'] = dialog_texts
    else:
        thread_message_history[thread_ts]['dialog_texts'] = [message_str]

def extract_urls_from_event(event):
    urls = set()
    for block in event['blocks']:
        for element in block['elements']:
            for e in element['elements']:
                if e['type'] == 'link':
                    url = urlparse(e['url']).geturl()
                    urls.add(url)
    return list(urls)

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    user = event["user"]
    thread_ts = event["ts"]

    parent_thread_ts = event["thread_ts"] if "thread_ts" in event else thread_ts
    if parent_thread_ts not in thread_message_history:
        thread_message_history[parent_thread_ts] = { 'dialog_texts': [], 'context_urls': set()}

    if "text" in event:
        update_thread_history(parent_thread_ts, 'User: %s' % insert_space(event["text"].replace('<@U04TCNR9MNF>', '')), extract_urls_from_event(event))
    
    urls = thread_message_history[parent_thread_ts]['context_urls']

    logger.info('=====> Current thread conversation messages are:')
    logger.info(thread_message_history[parent_thread_ts])

    # TODO: https://github.com/jerryjliu/llama_index/issues/778
    # if it can get the context_str, then put this prompt into the thread_message_history to provide more context to the chatGPT
    if len(extract_urls_from_event(event)) > 0: # if this conversation has urls, use llama with all urls in this thread
        future = executor.submit(get_answer_from_llama_web, thread_message_history[parent_thread_ts]['dialog_texts'], list(urls), logger)
    else:
        future = executor.submit(get_answer_from_chatGPT, thread_message_history[parent_thread_ts]['dialog_texts'], logger)

    try:
        gpt_response = future.result(timeout=300)
        update_thread_history(parent_thread_ts, 'AI: %s' % insert_space(f'{gpt_response}'))
        logger.info(gpt_response)
        say(f'<@{user}>, {gpt_response}', thread_ts=thread_ts)
    except concurrent.futures.TimeoutError:
        future.cancel()
        err_msg = 'Task timedout(5m) and was canceled.'
        logger.warning(err_msg)
        say(f'<@{user}>, {err_msg}', thread_ts=thread_ts)

register_slack_slash_commands(slack_app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
