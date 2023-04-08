from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader, PyPDFLoader

text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=0)

def text_load_and_split(filename):
    loader = UnstructuredFileLoader(filename)
    return text_splitter.split_documents(loader.load())

def pdf_load_and_split(filename):
    return PyPDFLoader(filename).load_and_split()