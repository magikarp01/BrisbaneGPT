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
# old key # os.environ["OPENAI_API_KEY"] = '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'
persist_directory="./embeddings"

embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

romeoandjuliet_qa = ChatVectorDBChain.from_llm(OpenAI(temperature=0, 
    model_name="gpt-3.5-turbo"), vectordb, return_source_documents=True)

chat_history=[]

query = "Have Romeo and Juliet spent the night together? Provide a verbose answer, referencing passages from the book."
result = romeoandjuliet_qa({"question": query, "chat_history": chat_history})
answer = result["answer"]
print(answer)
chat_history.append((query, answer))

"""
def find_similar_documents(query, vectordb, embeddings, top_k=5):
    query_embedding = embeddings.embed_text(query)
    similar_docs = vectordb.most_similar(query_embedding, top_k=top_k)
    return similar_docs


openai.api_key = os.environ["OPENAI_API_KEY"]

def chat_with_gpt(query):
    similar_docs = find_similar_documents(query, vectordb, embeddings)

    # You can customize the prompt based on the similar documents found
    prompt = f"{query}\n\n"
    for index, (similarity, doc) in enumerate(similar_docs):
        prompt += f"Document {index + 1}: {doc}\n\n"

    # Set up the API call parameters
    gpt_response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )

    return gpt_response.choices[0].text.strip()

response = chat_with_gpt("What is the theme of Romeo and Juliet?")
print(response)
"""