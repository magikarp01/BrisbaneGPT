from git import Repo
from embed_files import 


store_dir = "./sample-files/sample-repos"
def chat_repo(git_url):
    Repo.clone_from(git_url, store_dir)

