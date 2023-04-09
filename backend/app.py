from flask import Flask, request, jsonify, make_response
import json
from pathlib import Path

import sys
import os
sys.path.append(os.getcwd())

from directorygpt.embed_files import generate_embeddings
from directorygpt.chat_files import make_chatbot, ask_query

app = Flask(__name__)
embeddings_directory = os.path.abspath("./embeddings")
qa = make_chatbot(embeddings_directory)

@app.route('/', methods=["GET"])
def hello():
    return "Server active."

@app.route('/file', methods=['POST'])
def file():
    global qa

    path = request.json['path']
    generate_embeddings(embeddings_directory, path)
    qa = make_chatbot(embeddings_directory)
    result = True # TODO
    if result:
        return '', 200
    else:
        return '', 400

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    result = ask_query(qa, query)
    answer = result["answer"]
    return jsonify({"response": answer}), 200

if __name__ == '__main__':
    app.run(port=8000)
