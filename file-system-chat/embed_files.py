import os
import glob
from pathlib import Path
import platform

import loaders

from dotenv import load_dotenv
import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain


load_dotenv()


def file_load_and_split(filename):
    path = Path(filename)
    if path.suffix == ".txt":
        return loaders.text_load_and_split(filename)
    elif path.suffix == ".pdf":
        return loaders.pdf_load_and_split(filename)

def dir_load_and_split(dirname):
    all_docs = []
    for file in glob.glob('**/*', recursive=True):
        all_docs.extend(file_load_and_split(file))


def mark_docs(docs):
    for doc in docs:
        doc.page_content = f'Source filepath is {doc.metadata["source"]} for: "{doc.page_content}"'
    return docs


def generate_embeddings():
    persist_directory="./embeddings/sample-dir"
    embeddings = OpenAIEmbeddings()
    
    docs = mark_docs(dir_load_and_split("sample-files"))
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    vectordb.persist()
