from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    response = {"response": f"Your message was: {message}"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
