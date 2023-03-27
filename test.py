from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api-endpoint', methods=['POST'])
def receive_message():
    received_data = request.get_json()
    challenge = received_data['challenge']
    print(challenge)
    response_data = {'challenge': challenge}
    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)