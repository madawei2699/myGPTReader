#!/usr/bin/env python3.8
import requests
from event import EventManager
from flask import Flask, jsonify
from utils import setup_logger
from config import VERIFICATION_TOKEN, ENCRYPT_KEY
from handlers import request_url_verify_handler, message_receive_event_handler

logger = setup_logger('my_gpt_reader_server')

app = Flask(__name__)

event_manager = EventManager()
event_manager.register("url_verification")(request_url_verify_handler)
event_manager.register("im.message.receive_v1")(message_receive_event_handler)


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
