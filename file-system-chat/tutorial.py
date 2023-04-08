import os
import platform

import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import GutenbergLoader

print('Python:', platform.python_version())

os.environ["OPENAI_API_KEY"] = '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'
persist_directory="./embeddings"

def get_gutenberg(url):
    loader = GutenbergLoader(url)
    data = loader.load()
    return data

romeoandjuliet_data = get_gutenberg('https://www.gutenberg.org/cache/epub/1513/pg1513.txt')

text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
romeoandjuliet_doc = [text_splitter.split_documents(romeoandjuliet_data)[0]]

embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(romeoandjuliet_doc, embeddings, persist_directory=persist_directory)
vectordb.persist()
