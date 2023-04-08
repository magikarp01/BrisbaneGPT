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
persist_directory="./embeddings/sample-dir"

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

try:
    file_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, 
        model_name="gpt-3.5-turbo"), vectordb, return_source_documents=True)
except:
    print("Failed query")

chat_history=[]

def ask_query(query, chat_history):
    result = file_qa({"question": query, "chat_history": chat_history})
    answer = result["answer"]
    print(answer)
    chat_history.append((query, answer))
    return result

# query = "How can I make a trade when one of my orders was filled? Also, what question did I ask about Romeo and Juliet? Also, do you know the metadata of the files that you got this information from?"
# query = "How can I make a trade when one of my orders was filled? Also, do you know what files you got this information from?"
# query = "Also, what question did I ask about Romeo and Juliet? Can you identify which text file this question is in?"
query = "What school am I attending right now? Also, what do I have to do in my CS project? What files did you use to answer these questions?"
ask_query(query, chat_history)