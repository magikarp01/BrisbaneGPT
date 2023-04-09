from git import Repo
from embed_files import generate_embeddings
import chat_files

# generate_repo_embeddings("https://github.com/magikarp01/ml-from-scratch.git")
# generate_repo_embeddings("https://github.com/Torantulino/Auto-GPT.git")
# store_repo_dir = "./demo-files/autogpt-repo"
# store_embeddings_dir = "./embeddings/sample-repos/autogpt-repo"

# repo_name = "engshell"
repo_name = "autogpt"
store_repo_dir = "./demo-files/"+repo_name
store_embeddings_dir = "./embeddings/sample-repos/"+repo_name


def generate_repo_embeddings(git_url, chunk_size=500):
    try:
        Repo.clone_from(git_url, store_repo_dir)
    except:
        print("couldn't clone repo")
        pass
    generate_embeddings(store_embeddings_dir, store_repo_dir, chunk_size=chunk_size)

# generate_repo_embeddings("https://github.com/emcf/engshell.git", chunk_size=500)
# generate_repo_embeddings("https://github.com/Torantulino/Auto-GPT.git", chunk_size=500)

file_chatbot = chat_files.make_chatbot(store_embeddings_dir, top_k_docs=8)
queries = [
    "How can I spin up an autonomous instance of GPT4 for my own purposes using Auto-GPT?",
    "How does Auto-GPT maintain memory of its actions?",
    "Which file interacts with the OpenAI API in Auto-GPT?",
    "What pip packages does Auto-GPT require?"
]
for query in queries:
    print(f"Asking query {query}")
    result = chat_files.ask_query(file_chatbot, query)
    print("\n\n\n")

