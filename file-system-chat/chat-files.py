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
from langchain.document_loaders import GutenbergLoader

print('Python:', platform.python_version())

load_dotenv()
persist_directory="./embeddings/rtg"

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

print(vectordb)
file_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, 
    model_name="gpt-3.5-turbo"), vectordb)

chat_history=[]

query = "How can I make a trade when one of my orders was filled?"
result = file_qa({"question": query, "chat_history": chat_history})
answer = result["answer"]
print(answer)
chat_history.append((query, answer))
