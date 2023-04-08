from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import UnstructuredFileLoader, DirectoryLoader, PyPDFLoader

text_splitter = TokenTextSplitter(chunk_size=500, chunk_overlap=0)

def text_load_and_split(read_fname, sys_fname = None):
    loader = UnstructuredFileLoader(read_fname)
    docs = text_splitter.split_documents(loader.load())

    if sys_fname:
        for doc in docs:
            doc.metadata["source"] = sys_fname
    return docs

def pdf_load_and_split(filename):
    return PyPDFLoader(filename).load_and_split()