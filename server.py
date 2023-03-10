from flask import Flask, jsonify, request
import re
import os
import openai
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from llama_index import GPTSimpleVectorIndex, LLMPredictor, TrafilaturaWebReader
from langchain.chat_models import ChatOpenAI

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

slack_app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)
slack_handler = SlackRequestHandler(slack_app)

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


def extract_urls(text):
    urls = []
    words = text.split()
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            urls.append(word)
    return urls

def get_answer_from_chatGPT(message):
    message_normalized = insert_space(message)
    urls = extract_urls(message_normalized)
    if len(urls) > 0:
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
        documents = TrafilaturaWebReader().load_data(urls)
        index = GPTSimpleVectorIndex(documents)
        response = index.query(message_normalized, llm_predictor=llm_predictor)
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_normalized}]
        )
        print(completion.usage)
        response = completion.choices[0].message.content
    return response

@app.route('/chat', methods=['POST'])
def chat():
    response = {"response": f"{get_answer_from_chatGPT(request.json['message'])}"}
    return jsonify(response)

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    logger.info(event)
    user = event["user"]
    text = event["text"]
    user_message = text.replace('<@U04TCNR9MNF>', '')
    gpt_response =  get_answer_from_chatGPT(user_message)
    say(f'<@{user}>, ' + gpt_response)

if __name__ == '__main__':
    app.run(debug=True)
