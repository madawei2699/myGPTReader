#!/usr/bin/env python3.8
import os
import requests
import json
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
from utils import extract_text_and_links_from_content,insert_space,setup_logger,extract_post_text_and_links_from_content
from gpt import get_answer_from_chatGPT, get_answer_from_llama_web, get_answer_from_llama_file

# load env parameters form file named .env
load_dotenv(find_dotenv())
# 对于计算密集型任务，将 max_workers 设置为系统 CPU 核心数可能是一个更合适的选择。
# executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
# 创建一个日志器
logger = setup_logger('my_gpt_reader_server')

app = Flask(__name__)

# load from env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENCRYPT_KEY = os.getenv("ENCRYPT_KEY")
LARK_HOST = os.getenv("LARK_HOST")

# init service
message_api_client = MessageApiClient(APP_ID, APP_SECRET, LARK_HOST)
event_manager = EventManager()

thread_message_history = {}
MAX_THREAD_MESSAGE_HISTORY = 10

def update_thread_history(thread_id, message_str=None, urls=None, file=None):
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

@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    event = req_data.event;
    sender_id = event['event']["sender"]["sender_id"]
    message = event['event']["message"]
    create_time = event['header']["create_time"]
    message_type = message["message_type"]
    logger.info(f'message_type-{message_type}')
    if message_type != "text" and message_type != "post":
        logger.warning("Other types of messages have not been processed yet")
        message_api_client.reply_text_with_message_id(thread_id, json.dumps({"text": f'不接受如下类型为：{message["message_type"]}的消息'}), create_time)
        return jsonify()

    open_id = sender_id["open_id"]
    text_content = json.loads(message["content"])

    thread_id = message["message_id"]
    parent_thread_id = thread_id
    try:
        parent_thread_id = message.get("root_id", thread_id)
        # print(f'parent_id is: {message["parent_id"]}, message_id is: {thread_id}')
        # print(f'root_id is: {message["root_id"]}, message_id is: {thread_id}')
        # print(f'parent_thread_id is: {parent_thread_id}')
    except Exception:
        print(f"Root_id not found, using message_id as parent_thread_id {thread_id}")
    # 初始化 history
    if parent_thread_id not in thread_message_history:
        thread_message_history[parent_thread_id] = { 'dialog_texts': [], 'context_urls': set(), 'file': None}
    # 提取用户输入的内容更新到 thread_history
    result = None
    if message_type == 'text':
        if "text" in text_content:
            result = extract_text_and_links_from_content(text_content)
    elif message_type == 'post':
        if "content" in text_content:
            result = extract_post_text_and_links_from_content(text_content)
    item_text = result["text"]
    item_urls = result["link"]
    update_thread_history(parent_thread_id, item_text, item_urls)
    # 从 thread_history 中提取内容开始请求
    urls = thread_message_history[parent_thread_id]['context_urls']
    file = thread_message_history[parent_thread_id]['file']
    text = thread_message_history[parent_thread_id]['dialog_texts']
    logger.info('=====> Current thread conversation messages are:')
    logger.info(thread_message_history[parent_thread_id])
    try:
        if file is not None:
            gpt_response = get_answer_from_llama_file(dialog_context_keep_latest(text), file)
        elif len(urls) > 0:
            gpt_response = get_answer_from_llama_web(text, list(urls))
        else:
            gpt_response = get_answer_from_chatGPT(text)
        
        update_thread_history(parent_thread_id, ['AI: %s' % insert_space(f'{gpt_response}')])
        logger.info(f"请求成功-接下来调用接口发送消息")
        message_api_client.reply_text_with_message_id(thread_id, json.dumps({"text": f'{str(gpt_response)}'}), create_time)
        # if voicemessage is None:
        #     say(f'<@{user}>, {gpt_response}', thread_ts=thread_ts)
        # else:
        #     voice_file_path = get_voice_file_from_text(str(gpt_response))
        #     logger.info(f'=====> Voice file path is {voice_file_path}')
        #     slack_app.client.files_upload_v2(file=voice_file_path, channel=channel, thread_ts=parent_thread_ts)
    except Exception as e:
        err_msg = f'Task failed with error: {e}'
        print(err_msg)
        message_api_client.reply_text_with_message_id(thread_id, json.dumps({"text": f'<@{open_id}>, {err_msg}'}), create_time)
        # say(f'<@{user}>, {err_msg}', thread_ts=thread_ts)
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logger.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/api-endpoint", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    logger.info('=====> api-endpoint !')
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)
    if event_handler is None:
        return jsonify()
    return event_handler(event)


if __name__ == "__main__":
    # init()
    app.run(host="0.0.0.0", port=5000)
