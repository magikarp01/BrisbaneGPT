from git import Repo
from embed_files import generate_embeddings
import chat_files

store_repo_dir = "./demo-files/autogpt-repo"
store_embeddings_dir = "./embeddings/sample-repos/autogpt-repo"
def generate_repo_embeddings(git_url, chunk_size=300):
    try:
        Repo.clone_from(git_url, store_repo_dir)
    except:
        print("couldn't clone repo")
        pass
    generate_embeddings(store_embeddings_dir, store_repo_dir, chunk_size=chunk_size)

# generate_repo_embeddings("https://github.com/magikarp01/ml-from-scratch.git")
# generate_repo_embeddings("https://github.com/Torantulino/Auto-GPT.git")
file_chatbot = chat_files.make_chatbot("./embeddings/sample-repos/autogpt-repo", top_k_docs=8)
chat_history = []
query = "Can you explain what this github repository does?"
result = chat_files.ask_query(file_chatbot, query, chat_history)

