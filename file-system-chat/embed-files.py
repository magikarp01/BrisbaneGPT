import os
import platform

from dotenv import load_dotenv
import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader


load_dotenv()
# persist_directory="./embeddings/rtg"
persist_directory="./embeddings/sample-dir"
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings()
# vectordb = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

def text_loader(filename):
    # with open(filename, 'r') as f:
        # return f.read()
    return UnstructuredFileLoader(filename)

def dir_loader(dirname):
    return DirectoryLoader(dirname)

# rtg_text = text_loader("./sample-files/rtg.txt").load()
# print(rtg_text)
# rtg_docs = text_splitter.split_documents(rtg_text)

dir_text = dir_loader("sample-files").load()
dir_docs = text_splitter.split_documents(dir_text)

# vectordb = Chroma.from_documents(rtg_docs, embeddings, persist_directory=persist_directory)
vectordb = Chroma.from_documents(dir_docs, embeddings, persist_directory=persist_directory)
# vectordb.add_documents(rtg_docs)
# vectordb.persist()
