import os
import glob
from pathlib import Path
import platform
import tempfile
from git import Repo
from urllib.parse import urlparse

from dotenv import load_dotenv

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import TokenTextSplitter
from langchain.document_loaders import PyPDFLoader, UnstructuredFileLoader, UnstructuredPowerPointLoader, UnstructuredWordDocumentLoader

load_dotenv()

def text_load_and_split(read_fname, text_splitter, sys_fname = None):
    loader = UnstructuredFileLoader(read_fname)
    docs = text_splitter.split_documents(loader.load())

    if sys_fname:
        for doc in docs:
            doc.metadata["source"] = sys_fname
    return docs

# if text splitter is not specified, docs will be split by page (unknown chunk size)
# if text splitter is specified, docs no longer have page number
def pdf_load_and_split(filename, text_splitter=None):
    return PyPDFLoader(filename).load_and_split(text_splitter=text_splitter)

def worddoc_load_and_split(filename, text_splitter=None): 
    return UnstructuredWordDocumentLoader(filename, mode="elements").load_and_split(text_splitter=text_splitter)

def pptx_load_and_split(filename, text_splitter=None):
    return UnstructuredPowerPointLoader(filename, mode="elements").load_and_split(text_splitter=text_splitter)

def file_load_and_split(filename, text_splitter):
    path = Path(filename)
    if path.suffix == ".txt":
        return text_load_and_split(filename, text_splitter=text_splitter)
    elif path.suffix == ".pdf":
        return pdf_load_and_split(filename)
    elif path.suffix == ".docx":
        return worddoc_load_and_split(filename)
    elif path.suffix == ".pptx":
        return pptx_load_and_split(filename)
    elif path.suffix in [".py", ".c", ".java"]:
        with open(filename, 'r') as f:
            # Create a temporary file with a .txt suffix
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tf:
                # Write the contents of the Python file to the temporary file
                tf.write(f.read().encode('utf-8'))
                # Get the name of the temporary file
                return text_load_and_split(tf.name, text_splitter=text_splitter, sys_fname=filename)
    else:
        return []

def dir_load_and_split(dirname, text_splitter):
    all_docs = []
    for file in glob.glob(f'{dirname}/**/*', recursive=True):
        print(file)
        all_docs.extend(file_load_and_split(file, text_splitter=text_splitter))
    return all_docs


def repo_load(git_url, store_repo_dir):
    try:
        Repo.clone_from(git_url, store_repo_dir)
    except:
        pass


def load_and_split(fname, text_splitter):
    if bool(urlparse(fname).scheme):
        dir_name = fname.split('/')[-1]
        repo_load(fname, f"./git-repos/{fname.split('/')[-1]}")
        return load_and_split(dir_name, text_splitter=text_splitter)
    if os.path.isdir(fname):
        return dir_load_and_split(fname, text_splitter=text_splitter)
    elif os.path.isfile(fname):
        return file_load_and_split(fname, text_splitter=text_splitter)
    else:
        return []

def mark_docs(docs):
    for doc in docs:
        if "page" in doc.metadata:
            page = doc.metadata["page"]
            doc.page_content = f'Source filepath is {doc.metadata["source"]} on page {page+1} for: "{doc.page_content}"'
        else:
            doc.page_content = f'Source filepath is {doc.metadata["source"]} for: "{doc.page_content}"'
    return docs

def generate_embeddings(persist_dir, source, chunk_size=500):
    embeddings = OpenAIEmbeddings()
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=0) 

    docs = load_and_split(source, text_splitter=text_splitter)
    docs = mark_docs(docs)
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    vectordb.persist()

if __name__ == '__main__':
    generate_embeddings('./embeddings/sample-dir', "./sample-files", chunk_size=500)

