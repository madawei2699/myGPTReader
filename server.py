from flask import Flask, request
import re
import os
import openai
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from llama_index import GPTListIndex, LLMPredictor, TrafilaturaWebReader
from llama_index.prompts.default_prompts import DEFAULT_REFINE_PROMPT
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

def get_answer_from_chatGPT(message, logger):
    message_normalized = insert_space(message)
    urls = extract_urls(message_normalized)
    if len(urls) > 0:
        logger.info('=====> Use llama with chatGPT to answer!')
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
        documents = TrafilaturaWebReader().load_data(urls)
        logger.info(documents)
        index = GPTListIndex(documents)
        response = index.query(message_normalized, llm_predictor=llm_predictor, refine_template=DEFAULT_REFINE_PROMPT, similarity_top_k=5)
    else:
        logger.info('=====> Use chatGPT to answer!')
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_normalized}]
        )
        logger.info(completion.usage)
        response = completion.choices[0].message.content
    return response

@slack_app.event("app_mention")
def handle_mentions(event, say, logger):
    logger.info(event)
    user = event["user"]
    text = event["text"]
    user_message = text.replace('<@U04TCNR9MNF>', '')
    gpt_response =  get_answer_from_chatGPT(user_message, logger)
    say(f'<@{user}>, ' + gpt_response)

if __name__ == '__main__':
    app.run(debug=True)
