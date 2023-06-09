import warnings
warnings.filterwarnings("ignore") # lol


import os
import platform

from dotenv import load_dotenv
import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

print('Python:', platform.python_version())

load_dotenv()


def make_chatbot(embeddings_directory, top_k_docs=5):
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory=embeddings_directory, embedding_function=embeddings)

    try:
        file_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, 
            model_name="gpt-3.5-turbo"), vectordb, return_source_documents=True,
            top_k_docs_for_context=top_k_docs)
    except:
        print("Not enough docs")
    
    return file_qa


def ask_query(chat_db_chain, query, chat_history=None, default_prompt=None):
    if default_prompt == None:
        default_prompt = " Write your answer first without any sources, then use bullet points to LIST the sources (and pages) you got your information from at the end. ONLY list your sources at the end if you know how to answer. If you don't know how to answer, do not list sources. This is very important, you MUST put curly braces '{}' around only the source filepath. Do not put curly braces '{}' around the page number."
    if chat_history == None:
        chat_history = []
    query += default_prompt
    result = chat_db_chain({"question": query, "chat_history": chat_history})
    answer = result["answer"]
    print(answer)
    chat_history.append((query, answer))
    return result

if __name__ == '__main__':
    
    persist_directory="./embeddings/sample-dir"
    # query = "How can I make a trade when one of my orders was filled? Also, what question did I ask about Romeo and Juliet? Also, do you know which filepaths you got this information from?"
    # query = "Also, what question did I ask about Romeo and Juliet? Can you identify which text file this question is in?"
    # query = "What school am I attending right now? Also, what is my University Login ID for my vim/nano homework? What files did you use to answer these questions?"
    query = "What are the data structure requirements for my CS project? What file and page number did you find this on?"
    # query = "What does get_module_name do? What file is this in?"
    file_qa = make_chatbot(persist_directory, top_k_docs=7)
    chat_history = []
    result = ask_query(file_qa, query, chat_history)
