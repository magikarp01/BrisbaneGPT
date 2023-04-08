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
# persist_directory="./embeddings/rtg"
persist_directory="./embeddings/sample-dir"

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

file_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, 
    model_name="gpt-3.5-turbo"), vectordb, return_source_documents=True)

chat_history=[]

query = "How can I make a trade when one of my orders was filled? Can you identify which text file you're getting your answer from?"
result = file_qa({"question": query, "chat_history": chat_history})
answer = result["answer"]
print(answer)
chat_history.append((query, answer))

query = "Also, what question did I ask about Romeo and Juliet? Can you identify which text file this question is in?"
result = file_qa({"question": query, "chat_history": chat_history})
answer = result["answer"]
print(answer)
chat_history.append((query, answer))
