import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as mbox
from git import Repo
import shutil
import subprocess
import requests
import re
import stat

def remove_existing_folders(directory):
    """Remove existing 'SimpsPack' and 'SIMPS-SMP-Pack' folders if they exist."""
    simps_pack_dir = os.path.join(directory, "SimpsPack")
    simps_smp_pack_dir = os.path.join(directory, "SIMPS-SMP-Pack")
    for folder in [simps_pack_dir, simps_smp_pack_dir]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

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

def remove_git_directory(directory):
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    for root, dirs, files in os.walk(directory):
        for name in dirs:
            dir_path = os.path.join(root, name)
            # Remove read-only attribute from directories
            os.chmod(dir_path, stat.S_IWRITE)
        for name in files:
            file_path = os.path.join(root, name)
            # Remove read-only attribute from files
            os.chmod(file_path, stat.S_IWRITE)

    # Remove the directory and its contents
    shutil.rmtree(directory, onerror=remove_readonly)


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
    # Remove the SimpsPack directory if it exists
    simps_pack_dir = os.path.join(directory, "SimpsPack")
    if os.path.exists(simps_pack_dir):
        shutil.rmtree(simps_pack_dir)
        print("Removed existing SimpsPack directory.")
    
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
            print("SimpsPack Auto-Download Wizard", f"Extraction completed and SIMPS-SMP-Pack folder cleaned up.\nLatest Commit Version: {first_commit_message}")
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

        # Check if there are local commit messages available
        git_folder = os.path.join(directory, "SimpsPack", ".git")  # Adjusted path here
        local_commit_message = extract_first_commit_message(git_folder)

        if local_commit_message is not None:
            # Local commit message is available, compare versions
            print("Checking if repository is up to date...")
            latest_commit_message = get_latest_commit_message(repo_url)
            if latest_commit_message is None:
                print("Error retrieving latest commit message. Aborting download.")
                mbox.showerror("Error", "Failed to retrieve latest commit message. Please try again later.")
                return

            latest_version = extract_version(latest_commit_message)
            local_version = extract_version(local_commit_message)

            print(f"Latest commit version: {latest_version}")
            print(f"Local commit version: {local_version}")

            if local_version == latest_version:
                # Display message indicating that the repository is up to date
                mbox.showinfo("SimpsPack Auto-Download Wizard", "The SimpsPack is already up to date.")
                print("Repository is already up to date. Aborting download.")
                return
        # Delete existing files
        remove_existing_folders(directory)
        
        # Clone the repository if it's not up to date or local commit messages are not available
        clone_github_repo(repo_url, target_dir)

        # Extract SimpsPack folder and cleanup
        extract_and_cleanup(directory, repo_url)

        # Close the wizard after confirmation
        first_commit_message = extract_first_commit_message(git_folder)
        if first_commit_message:
            mbox.showinfo("SimpsPack Auto-Download Wizard", f"Download completed successfully and SIMPS-SMP-Pack folder cleaned up.\nLatest Commit Version: {first_commit_message}")
            root.destroy()
        else:
            print("Failed to extract the first commit message.")
            mbox.showerror("Error", "Failed to extract the first commit message.")
            
    else:
        print("Please select a directory first.")




# Default directory
default_directory = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", ".minecraft", "resourcepacks")

# GUI setup
root = tk.Tk()
root.title("SimpsPack Auto-Download Wizard")

# Set initial window size
root.geometry("600x300")

# Main label and entry for directory selection
label = tk.Label(root, text="Select directory:")
label.pack(pady=5)

entry = tk.Entry(root, width=70)
entry.insert(0, default_directory)
entry.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=select_directory)
browse_button.pack(pady=5)

create_button = tk.Button(root, text="Auto-Download SimpsPack", command=create_hello_file)
create_button.pack(pady=5)

# Additional entry for text input
additional_text = "Encounter any problems? Message me at:\n@BouncingElf10 -- On Discord\n168445249+BouncingElf10@users.noreply.github.com -- On Email"
additional_text_widget = tk.Text(root, wrap="word", height=4, width=60)
additional_text_widget.insert(tk.END, additional_text)
additional_text_widget.pack(pady=5)

root.mainloop()
