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
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader, PyPDFLoader


load_dotenv()
# persist_directory="./embeddings/rtg"
persist_directory="./embeddings/sample-dir"
text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings()
# vectordb = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

def text_load_and_split(filename):
    loader = UnstructuredFileLoader(filename)
    return text_splitter.split_documents(loader.load())

def pdf_load_and_split(filename):
    return PyPDFLoader(filename).load_and_split()

def dir_load_and_split(dirname):
    loader = DirectoryLoader(dirname)
    return text_splitter.split_documents(loader.load())

def mark_docs(docs):
    for doc in docs:
        doc.page_content = f'Information from: {doc.metadata["source"]}. {doc.page_content}'
    return docs


# docs = mark_docs(dir_load_and_split("sample-files"))
docs = mark_docs(pdf_load_and_split("sample-files/project7_decoded.pdf"))

# vectordb = Chroma.from_documents(rtg_docs, embeddings, persist_directory=persist_directory)
vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
# vectordb.add_documents(rtg_docs)
vectordb.persist()
