import os
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as mbox
from git import Repo
import shutil
import subprocess
import requests
import re


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
        print("wotks:", commit_message)
    else:
        print("Failed to fetch commit message:", response.text)
        return None