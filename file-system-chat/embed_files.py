import os
import glob
from pathlib import Path
import platform
import tempfile
from git import Repo
from urllib.parse import urlparse

import loaders

from dotenv import load_dotenv
import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain

load_dotenv()

def file_load_and_split(filename):
    path = Path(filename)
    if path.suffix == ".txt":
        return loaders.text_load_and_split(filename)
    elif path.suffix == ".pdf":
        return loaders.pdf_load_and_split(filename)
    elif path.suffix in [".py", ".c", "."]:
        with open(filename, 'r') as f:
            # Create a temporary file with a .txt suffix
            with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tf:
                # Write the contents of the Python file to the temporary file
                tf.write(f.read().encode('utf-8'))
                # Get the name of the temporary file
                return loaders.text_load_and_split(tf.name, filename)
    else:
        return []

def dir_load_and_split(dirname):
    all_docs = []
    for file in glob.glob(f'{dirname}/**/*', recursive=True):
        print(file)
        all_docs.extend(file_load_and_split(file))
    return all_docs


def repo_load(git_url, store_repo_dir):
    try:
        Repo.clone_from(git_url, store_repo_dir)
    except:
        pass
    


def load_and_split(fname):
    if bool(urlparse(fname).scheme):
        dir_name = fname.split('/')[-1]
        repo_load(fname, f"./git-repos/{fname.split('/')[-1]}")
        return load_and_split(dir_name)
    if os.path.isdir(fname):
        return dir_load_and_split(fname)
    elif os.path.isfile(fname):
        return file_load_and_split(fname)
    else:
        return None

def mark_docs(docs):
    for doc in docs:
        if "page" in doc.metadata:
            page = doc.metadata["page"]
            doc.page_content = f'Source filepath is {doc.metadata["source"]} on page {page+1} for: "{doc.page_content}"'
        else:
            doc.page_content = f'Source filepath is {doc.metadata["source"]} for: "{doc.page_content}"'
    return docs

def generate_embeddings(persist_dir, source_dir):
    embeddings = OpenAIEmbeddings()

    docs = load_and_split(source_dir)
    docs = mark_docs(docs)
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_dir)
    vectordb.persist()

if __name__ == '__main__':
    generate_embeddings('./embeddings/sample-dir', "./sample-files")


