from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/chat/hello')
def Hello_World():
    return 'Hello World!'


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

#