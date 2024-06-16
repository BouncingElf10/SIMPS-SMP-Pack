import os
import tkinter as tk
from tkinter import filedialog
from git import Repo
import shutil
import subprocess

def clone_github_repo(repo_url, target_dir):
    try:
        # Clone the repository
        Repo.clone_from(repo_url, target_dir)
        print(f"Repository cloned to {target_dir}")
    except Exception as e:
        print(f"Failed to clone repository: {str(e)}")

def select_directory():
    directory = filedialog.askdirectory(initialdir=default_directory)
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def get_latest_commit_message(repo_url):
    # Split the GitHub repository URL to extract username and repository name
    parts = repo_url.split('/')
    username = parts[-2]
    repo_name = parts[-1]

    # Make a request to GitHub API to get the latest commit information
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/commits/main"
    response = requests.get(api_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract and return the commit message
        commit_info = response.json()
        commit_message = commit_info['commit']['message']
        return commit_message
    else:
        print("Failed to fetch commit message:", response.text)
        return None

def extract_and_cleanup(directory):
    # Specify paths
    source_dir = os.path.join(directory, "SIMPS-SMP-Pack", "SimpsPack")
    destination_dir = os.path.join(directory, "SimpsPack")

    # Copy contents of SimpsPack folder to parent directory
    shutil.copytree(source_dir, destination_dir)

    # Move the .git directory into the SimpsPack folder
    git_dir = os.path.join(directory, "SIMPS-SMP-Pack", ".git")
    shutil.move(git_dir, destination_dir)

    # Remove the SIMPS-SMP-Pack directory contents
    simps_pack_dir = os.path.join(directory, "SIMPS-SMP-Pack")
    for item in os.listdir(simps_pack_dir):
        item_path = os.path.join(simps_pack_dir, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)
        else:
            os.remove(item_path)

    # Remove the SIMPS-SMP-Pack directory
    os.rmdir(simps_pack_dir)
    print("Extraction completed and SIMPS-SMP-Pack folder cleaned up.")



def create_hello_file():
    directory = entry.get()
    if directory:
        repo_url = "https://github.com/BouncingElf10/SIMPS-SMP-Pack.git"
        target_dir = os.path.join(directory, "SIMPS-SMP-Pack")
        clone_github_repo(repo_url, target_dir)
        
        # Extract SimpsPack folder and cleanup
        extract_and_cleanup(directory)
    else:
        print("Please select a directory first.")

# Default directory
default_directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks")

# GUI setup
root = tk.Tk()
root.title("SimpsPack Auto-Download Wizard")

label = tk.Label(root, text="Select directory:")
label.pack()

entry = tk.Entry(root, width=50)
entry.insert(0, default_directory)
entry.pack()

browse_button = tk.Button(root, text="Browse", command=select_directory)
browse_button.pack()

create_button = tk.Button(root, text="Auto-Download SimpsPack", command=create_hello_file)
create_button.pack()

root.mainloop()


