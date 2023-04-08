from git import Repo
from embed_files import generate_embeddings
import chat_files

store_repo_dir = "./sample-files/sample-repos"
store_embeddings_dir = "./embeddings/sample-repos"
def generate_repo_embeddings(git_url):
    try:
        Repo.clone_from(git_url, store_repo_dir)
    except:
        pass
    generate_embeddings(store_repo_dir, store_embeddings_dir)

# generate_repo_embeddings("https://github.com/magikarp01/ml-from-scratch.git")
file_chatbot = chat_files.make_chatbot("./embeddings/sample-repos", top_k_docs=3)
chat_history = []
query = "What files have information/implementations for fully connected layers and convolutional layers?"
result = chat_files.ask_query(file_chatbot, query, chat_history)
print(result)
