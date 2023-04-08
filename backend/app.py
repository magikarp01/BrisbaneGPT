from flask import Flask, request, jsonify, make_response
import json

def dummy_file(path):
    return True

def dummy_chat(query):
    return "hi"

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello():
    return "Server active."

@app.route('/file', methods=['POST'])
def file():
    path = request.form['path']
    result = dummy_file(path==path)
    if result:
        return '', 200
    else:
        return '', 400

@app.route('/chat', methods=['POST'])
def chat():
    query = request.form['query']
    result = dummy_chat(query=query)
    return jsonify({"answer": result}), 200

if __name__ == '__main__':
   app.run()