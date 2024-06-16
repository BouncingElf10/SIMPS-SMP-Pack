import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as mbox
from git import Repo
import shutil
import subprocess
import requests
import re

# Hide console window
import subprocess, sys
if getattr(sys, 'frozen', False):
    subprocess.Popen(["pythonw", sys.argv[0]], creationflags=subprocess.CREATE_NEW_CONSOLE)
    sys.exit()


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

def extract_version(commit_message):
    # Define a regex pattern to match version numbers
    pattern = r'(?:v)?(\d+\.\d+\.\d+)'

    # Search for the pattern in the commit message
    match = re.search(pattern, commit_message)
    if match:
        return match.group(1)
    else:
        return None

def create_hello_file():
    directory = entry.get()
    if directory:
        repo_url = "https://github.com/BouncingElf10/SIMPS-SMP-Pack"
        target_dir = os.path.join(directory, "SIMPS-SMP-Pack")

        # Check if the repository is already up to date
        print("Checking if repository is up to date...")
        latest_commit_message = get_latest_commit_message(repo_url)
        if latest_commit_message is None:
            #print("Error retrieving latest commit message. Aborting download.")
            mbox.showerror("Error", "Failed to retrieve latest commit message. Please try again later.")
            return

        print(f"Latest commit message from GitHub: {latest_commit_message}")
        latest_version = extract_version(latest_commit_message)
        if latest_version is None:
            print("No version number found in the latest commit message.")
            mbox.showwarning("Warning", "No version number found in the latest commit message.")
            return

        print(f"Latest version number: {latest_version}")

        # Extract the version number from the local commit message
        username = os.getlogin()
        git_folder = os.path.join(directory, "SIMPS-SMP-Pack", ".git")
        local_commit_message = extract_first_commit_message(git_folder)
        local_version = extract_version(local_commit_message)
        if local_version is None:
            print("No version number found in the local commit message.")
            mbox.showwarning("Warning", "No version number found in the local commit message.")
            return

        print(f"Local version number: {local_version}")

        # Compare the local and latest version numbers
        if local_version == latest_version:
            # Display message indicating that the repository is up to date
            mbox.showinfo("SimpsPack Auto-Download Wizard", "The repository is already up to date.")
            print("Repository is already up to date. Aborting download.")
            return

        # Clone the repository if it's not up to date
        print("Cloning repository...")
        clone_github_repo(repo_url, target_dir)
        
        # Extract SimpsPack folder and cleanup
        print("Extracting SimpsPack folder and cleaning up...")
        extract_and_cleanup(directory, repo_url)
    else:
        print("Please select a directory first.")



# Default directory
default_directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks")

# GUI setup
root = tk.Tk()
root.title("SimpsPack Auto-Download Wizard")

# Set initial window size
root.geometry("600x200")

label = tk.Label(root, text="Select directory:")
label.pack(pady=10)  # Add vertical padding to the label

entry = tk.Entry(root, width=70)  # Increase the width of the entry widget
entry.insert(0, default_directory)
entry.pack(pady=5)  # Add vertical padding to the entry field

browse_button = tk.Button(root, text="Browse", command=select_directory, padx=10, pady=5)
browse_button.pack(pady=5)  # Add vertical padding to the browse button

create_button = tk.Button(root, text="Auto-Download SimpsPack", command=create_hello_file, padx=10, pady=5)
create_button.pack(pady=5)  # Add vertical padding to the create button

root.mainloop()



