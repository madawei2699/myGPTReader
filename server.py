#!/usr/bin/env python3.8

import os
import logging
import requests
import json
from api import MessageApiClient
from event import MessageReceiveEvent, UrlVerificationEvent, EventManager
from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv
from utils import extract_link_and_text
import concurrent.futures
from gpt import get_answer_from_chatGPT, get_answer_from_llama_web

# load env parameters form file named .env
load_dotenv(find_dotenv())
executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)
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


@event_manager.register("url_verification")
def request_url_verify_handler(req_data: UrlVerificationEvent):
    # url verification, just need return challenge
    if req_data.event.token != VERIFICATION_TOKEN:
        raise Exception("VERIFICATION_TOKEN is invalid")
    return jsonify({"challenge": req_data.event.challenge})


@event_manager.register("im.message.receive_v1")
def message_receive_event_handler(req_data: MessageReceiveEvent):
    sender_id = req_data.event.sender.sender_id
    message = req_data.event.message
    if message.message_type != "text":
        logging.warn("Other types of messages have not been processed yet")
        return jsonify()
        # get open_id and text_content
    open_id = sender_id.open_id
    text_content = json.loads(message.content)
    print(text_content)
    if "text" in text_content:
        result = extract_link_and_text(text_content)
        text = result["text"]
        urls = result["link"]
        # 检查 urls 是否为 None
        if urls is None:
            urls = []
        if len(urls) > 0:
            future = executor.submit(get_answer_from_llama_web, text, list(urls))
        else:
            future = executor.submit(get_answer_from_chatGPT, text)
        try:
            gpt_response = future.result(timeout=300)
            print(f"请求成功：{type(gpt_response)}")
            message_api_client.send_text_with_open_id(open_id, json.dumps({"text": str(gpt_response)}))
            # if voicemessage is None:
            #     say(f'<@{user}>, {gpt_response}', thread_ts=thread_ts)
            # else:
            #     voice_file_path = get_voice_file_from_text(str(gpt_response))
            #     logger.info(f'=====> Voice file path is {voice_file_path}')
            #     slack_app.client.files_upload_v2(file=voice_file_path, channel=channel, thread_ts=parent_thread_ts)
        except concurrent.futures.TimeoutError:
            future.cancel()
            err_msg = 'Task timedout(5m) and was canceled.'
            print(err_msg)
            # say(f'<@{user}>, {err_msg}', thread_ts=thread_ts)
    
    return jsonify()


@app.errorhandler
def msg_error_handler(ex):
    logging.error(ex)
    response = jsonify(message=str(ex))
    response.status_code = (
        ex.response.status_code if isinstance(ex, requests.HTTPError) else 500
    )
    return response


@app.route("/api-endpoint", methods=["POST"])
def callback_event_handler():
    # init callback instance and handle
    event_handler, event = event_manager.get_handler_with_event(VERIFICATION_TOKEN, ENCRYPT_KEY)
    logging.info("/api-endpoint-------------")
    return event_handler(event)


if __name__ == "__main__":
    # init()
    app.run(host="0.0.0.0", port=5000)
