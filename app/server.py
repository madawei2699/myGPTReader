import logging
import re
import os
import requests
from urllib.parse import urlparse
from flask import Flask, request
from flask_apscheduler import APScheduler
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import concurrent.futures
from app.daily_hot_news import build_all_news_block
from app.gpt import get_answer_from_chatGPT, get_answer_from_llama_file, get_answer_from_llama_web, get_text_from_whisper, get_voice_file_from_text, index_cache_file_dir
from app.rate_limiter import RateLimiter
from app.slash_command import register_slack_slash_commands
from app.ttl_set import TtlSet
from app.util import md5

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
            reply_broadcast=True,
            unfurl_links=False,
            unfurl_media=False
        )

@scheduler.task('cron', id='daily_news_task', hour=1, minute=30)
def schedule_news():
    logging.info("=====> Start to send daily news!")
    all_news_blocks = build_all_news_block()
    send_daily_news(slack_app.client, all_news_blocks)

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

def update_thread_history(thread_ts, message_str=None, urls=None, file=None):
    if urls is not None:
        thread_message_history[thread_ts]['context_urls'].update(urls)
    if message_str is not None:
        if thread_ts in thread_message_history:
            dialog_texts = thread_message_history[thread_ts]['dialog_texts']
            dialog_texts.append(message_str)
            if len(dialog_texts) > MAX_THREAD_MESSAGE_HISTORY:
                dialog_texts = dialog_texts[-MAX_THREAD_MESSAGE_HISTORY:]
            thread_message_history[thread_ts]['dialog_texts'] = dialog_texts
        else:
            thread_message_history[thread_ts]['dialog_texts'] = [message_str]
    if file is not None:
        thread_message_history[thread_ts]['file'] = file

def extract_urls_from_event(event):
    urls = set()
    for block in event['blocks']:
        for element in block['elements']:
            for e in element['elements']:
                if e['type'] == 'link':
                    url = urlparse(e['url']).geturl()
                    urls.add(url)
    return list(urls)

whitelist_file = "app/data//vip_whitelist.txt"

filetype_extension_allowed = ['epub', 'pdf', 'text', 'docx', 'markdown', 'm4a', 'webm', 'mp3', 'wav']
filetype_voice_extension_allowed = ['m4a', 'webm', 'mp3', 'wav']
max_file_size = 3 * 1024 * 1024
temp_whitelist_users = TtlSet()
temp_whitelist_channle_id = 'C04VARAS1S7'

limiter_message_per_user = 10
limiter_time_period = 2 * 3600
limiter = RateLimiter(limit=limiter_message_per_user, period=limiter_time_period)

def is_authorized(user_id: str) -> bool:
    if user_id in temp_whitelist_users:
        return True
    with open(whitelist_file, "r") as f:
        return user_id in f.read().splitlines()
    
def dialog_context_keep_latest(dialog_texts, max_length=1):
    if len(dialog_texts) > max_length:
        dialog_texts = dialog_texts[-max_length:]
    return dialog_texts

def format_dialog_text(text, voicemessage=None):
    return insert_space(text.replace("<@U04TCNR9MNF>", "")) + ('\n' + voicemessage if voicemessage else '')

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    logger.info(event)

    user = event["user"]
    thread_ts = event["ts"]
    channel = event["channel"]

    file_md5_name = None
    voicemessage = None

    if not limiter.allow_request(user):
        if not is_authorized(user):
            say(f'<@{user}>, you have reached the limit of {limiter_message_per_user} messages {limiter_time_period / 3600} hour, please try again later.', thread_ts=thread_ts)
            return

    # temp whitelist handle
    if channel == temp_whitelist_channle_id:
        # add 1 hour play time, refresh temp whitelist when user mention bot in temp whitelist channel
        temp_whitelist_users.add(user, 60 * 60)

    if event.get('files'):
        if not is_authorized(event['user']):
            say(f'<@{user}>, this feature is only allowed by whitelist user, please contact the admin to open it.', thread_ts=thread_ts)
            return
        file = event['files'][0] # only support one file for one thread
        logger.info('=====> Received file:')
        logger.info(file)
        filetype = file["filetype"]
        if filetype not in filetype_extension_allowed:
            say(f'<@{user}>, this filetype is not supported, please upload a file with extension [{", ".join(filetype_extension_allowed)}]', thread_ts=thread_ts)
            return
        if file["size"] > max_file_size:
            say(f'<@{user}>, this file size is beyond max file size limit ({max_file_size / 1024 /1024}MB)', thread_ts=thread_ts)
            return
        url_private = file["url_private"]
        temp_file_path = index_cache_file_dir + user
        if not os.path.exists(temp_file_path):
            os.makedirs(temp_file_path)
        temp_file_filename = temp_file_path + '/' + file["name"]
        with open(temp_file_filename, "wb") as f:
            response = requests.get(url_private, headers={"Authorization": "Bearer " + slack_app.client.token})
            f.write(response.content)
            logger.info(f'=====> Downloaded file to save {temp_file_filename}')
            temp_file_md5 = md5(temp_file_filename)
            file_md5_name = index_cache_file_dir + temp_file_md5 + '.' + filetype
            if not os.path.exists(file_md5_name):
                logger.info(f'=====> Rename file to {file_md5_name}')
                os.rename(temp_file_filename, file_md5_name)
                if filetype in filetype_voice_extension_allowed:
                    voicemessage = get_text_from_whisper(file_md5_name)

    parent_thread_ts = event["thread_ts"] if "thread_ts" in event else thread_ts
    if parent_thread_ts not in thread_message_history:
        thread_message_history[parent_thread_ts] = { 'dialog_texts': [], 'context_urls': set(), 'file': None}

    if "text" in event:
        update_thread_history(parent_thread_ts, f'User: {format_dialog_text(event["text"], voicemessage)}', extract_urls_from_event(event))

    if file_md5_name is not None:
        if not voicemessage:
            update_thread_history(parent_thread_ts, None, None, file_md5_name)
    
    urls = thread_message_history[parent_thread_ts]['context_urls']
    file = thread_message_history[parent_thread_ts]['file']

    logger.info('=====> Current thread conversation messages are:')
    logger.info(thread_message_history[parent_thread_ts])

    # TODO: https://github.com/jerryjliu/llama_index/issues/778
    # if it can get the context_str, then put this prompt into the thread_message_history to provide more context to the chatGPT
    if file is not None:
        future = executor.submit(get_answer_from_llama_file, dialog_context_keep_latest(thread_message_history[parent_thread_ts]['dialog_texts']), file)
    elif len(urls) > 0:
        future = executor.submit(get_answer_from_llama_web, thread_message_history[parent_thread_ts]['dialog_texts'], list(urls))
    else:
        future = executor.submit(get_answer_from_chatGPT, thread_message_history[parent_thread_ts]['dialog_texts'])

    try:
        gpt_response = future.result(timeout=300)
        update_thread_history(parent_thread_ts, 'AI: %s' % insert_space(f'{gpt_response}'))
        logger.info(gpt_response)
        if voicemessage is None:
            say(f'<@{user}>, {gpt_response}', thread_ts=thread_ts)
        else:
            voice_file_path = get_voice_file_from_text(str(gpt_response))
            logger.info(f'=====> Voice file path is {voice_file_path}')
            slack_app.client.files_upload_v2(file=voice_file_path, channel=channel, thread_ts=parent_thread_ts)
    except concurrent.futures.TimeoutError:
        future.cancel()
        err_msg = 'Task timedout(5m) and was canceled.'
        logger.warning(err_msg)
        say(f'<@{user}>, {err_msg}', thread_ts=thread_ts)

register_slack_slash_commands(slack_app)
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)
