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
from langchain.document_loaders import UnstructuredFileLoader


load_dotenv()
persist_directory="./embeddings/rtg"
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings()
vectordb = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

def text_loader(filename):
    # with open(filename, 'r') as f:
        # return f.read()
    return UnstructuredFileLoader(filename)

rtg_text = text_loader("./sample-files/rtg.txt").load()
print(rtg_text)
rtg_docs = text_splitter.split_documents(rtg_text)

# vectordb.add_documents(rtg_docs)
# vectordb.persist()
