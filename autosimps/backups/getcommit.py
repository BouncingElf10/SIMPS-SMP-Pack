import subprocess
import os

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

# Example usage:
if __name__ == "__main__":
    username = os.getlogin()  # Get the current user's username
    git_folder = r'C:\Users\{}\AppData\Roaming\.minecraft\resourcepacks\SimpsPack\.git'.format(username)
    first_commit_message = extract_first_commit_message(git_folder)
    if first_commit_message:
        print("First Commit Message:")
        print("-", first_commit_message)
    else:
        print("Failed to extract the first commit message.")
