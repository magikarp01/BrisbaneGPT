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

