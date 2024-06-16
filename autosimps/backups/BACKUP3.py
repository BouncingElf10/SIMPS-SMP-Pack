import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as mbox
from git import Repo
import shutil
import subprocess
import requests

def clone_github_repo(repo_url, target_dir):
    try:
        # Clone the repository
        Repo.clone_from(repo_url, target_dir)
        print(f"SIMPS-SMP-Pack cloned to {target_dir}")
    except Exception as e:
        print(f"Failed to clone repository: {str(e)}")

def select_directory():
    directory = filedialog.askdirectory(initialdir=default_directory)
    if directory:
        entry.delete(0, tk.END)
        entry.insert(0, directory)

def extract_first_commit_message(git_folder):
    try:
        # Change directory to the git_folder
        os.chdir(git_folder)
        
        # Run 'git log' command to get the first commit message
        result = subprocess.run(['git', 'log', '--format=%s', '-1'], stdout=subprocess.PIPE)
        
        # Decode the result from bytes to string
        first_commit_message = result.stdout.decode('utf-8').strip()
        
        return first_commit_message
    except Exception as e:
        print("Error:", e)
        return None

def extract_and_cleanup(directory, repo_url):
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

    # Get the latest commit message
    if __name__ == "__main__":
        username = os.getlogin()  # Get the current user's username
        git_folder = r'C:\Users\{}\AppData\Roaming\.minecraft\resourcepacks\SimpsPack\.git'.format(username)
        first_commit_message = extract_first_commit_message(git_folder)
        if first_commit_message:
            # Show the commit message in a popup window
            mbox.showinfo("SimpsPack Auto-Download Wizard", f"Extraction completed and SIMPS-SMP-Pack folder cleaned up.\nLatest Commit Version: {first_commit_message}")
        else:
            print("Failed to extract the first commit message.")

def create_hello_file():
    directory = entry.get()
    if directory:
        repo_url = "https://github.com/BouncingElf10/SIMPS-SMP-Pack"
        target_dir = os.path.join(directory, "SIMPS-SMP-Pack")
        clone_github_repo(repo_url, target_dir)
        
        # Extract SimpsPack folder and cleanup
        extract_and_cleanup(directory, repo_url)
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


