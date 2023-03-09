from flask import Flask, jsonify, request
import re
import os
import openai
from llama_index import GPTSimpleVectorIndex, TrafilaturaWebReader
from llama_index.langchain_helpers.chatgpt import ChatGPTLLMPredictor

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)


def insert_space(text):

    # Handling the case between English words and Chinese characters
    text = re.sub(r'([a-zA-Z])([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])([a-zA-Z])', r'\1 \2', text)

    # Handling the situation between numbers and Chinese
    text = re.sub(r'(\d)([\u4e00-\u9fa5])', r'\1 \2', text)
    text = re.sub(r'([\u4e00-\u9fa5])(\d)', r'\1 \2', text)

    return text


def extract_urls(text):
    urls = []
    words = text.split()
    for word in words:
        if word.startswith("http://") or word.startswith("https://"):
            urls.append(word)
    return urls


@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    message_normalized = insert_space(message)
    urls = extract_urls(message_normalized)
    if len(urls) > 0:
        llm_predictor = ChatGPTLLMPredictor(temperature=0.2, prepend_messages=[
            {"role": "system", "content": "你是一名全能专家，对各类知识都非常了解。在做分析时，请尽可能做出深度的分析，不要重复话术，并使用多种句式，使内容看起来更加有说服力。另外如果问题是中文的，你就用中文回复，如果是英文的，就用英文回复。"},
        ])
        documents = TrafilaturaWebReader().load_data(urls)
        index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor)
        response = index.query(message_normalized)
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_normalized}]
        )
        print(completion.usage)
        response = completion.choices[0].message.content

    response = {"response": f"{response}"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
