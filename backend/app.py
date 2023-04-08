from flask import Flask, request, jsonify, make_response
import json

from directorygpt.embed_files import generate_embeddings
from directorygpt.chat_files import make_chatbot, ask_query

def dummy_file(path):
    return True

def dummy_chat(query):
    return "hi"

app = Flask(__name__)
embeddings_directory = "./embeddings"
chat_history = []
qa = make_chatbot(embeddings_directory)

@app.route('/', methods=["GET"])
def hello():
    return "Server active."

@app.route('/file', methods=['POST'])
def file():
    path = request.json['path']
    generate_embeddings(embeddings_directory, path)
    result = True # TODO
    if result:
        return '', 200
    else:
        return '', 400

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    result = ask_query(qa, query, chat_history)
    answer = result["answer"]
    return jsonify({"response": answer}), 200

if __name__ == '__main__':
   app.run(port=5000)