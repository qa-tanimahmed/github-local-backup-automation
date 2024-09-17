import os
import requests
import subprocess
import keyring
import shutil
import json
import platform
import stat
from getpass import getpass

# Constants for caching
GITHUB_SERVICE = 'github_backup'

# Get the current directory where the script is being run
BACKUP_DIR = os.path.dirname(os.path.realpath(__file__))

def get_github_credentials(use_cache=True):
    """Fetch GitHub credentials, either from cache or prompt the user."""
    if use_cache:
        username = keyring.get_password(GITHUB_SERVICE, 'username')
        password = keyring.get_password(GITHUB_SERVICE, 'password')  # This should be the PAT
        
        # Debugging print statements
        print(f"Cached username: {username}")
        print(f"Cached password: {'Exists' if password else 'None'}")
        
        if username and password:
            print("Using cached GitHub credentials.")
            return username, password

    # If cache is disabled or credentials not found, prompt the user
    username = input("Enter GitHub username: ")
    password = getpass("Enter GitHub personal access token (PAT): ")
    
    return username, password

def save_github_credentials(username, password):
    """Cache GitHub credentials in the keyring."""
    print("Saving credentials to cache...")
    keyring.set_password(GITHUB_SERVICE, 'username', username)
    keyring.set_password(GITHUB_SERVICE, 'password', password)

def authenticate_github(username, password):
    """Attempt to authenticate with GitHub using the provided credentials."""
    GITHUB_API_URL = 'https://api.github.com/user/repos'
    print("Attempting to authenticate with GitHub...")
    response = requests.get(GITHUB_API_URL, auth=(username, password))

    if response.status_code == 200:
        print("Authentication successful!")
        return response.json()  # Return the list of repositories
    elif response.status_code == 401:
        print("Invalid credentials. Please try again.")
        return None
    elif response.status_code == 403 and 'X-RateLimit-Remaining' in response.headers:
        print("Rate limit exceeded. Please wait and try again later.")
        print(f"Rate limit reset at: {response.headers['X-RateLimit-Reset']}")
        return None
    else:
        print(f"Failed to fetch repositories: {response.status_code}")
        return None


def make_writable(func, path, exc_info):
    """A helper function to force remove read-only files and directories."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_or_pull_repo(repo_url, repo_name):
    """Clone or pull the repository to the backup directory."""
    repo_dir = os.path.join(BACKUP_DIR, repo_name)

    if not os.path.exists(repo_dir):
        print(f'Cloning {repo_name}...')
        subprocess.run(['git', 'clone', repo_url, repo_dir])
    else:
        choice = input(f"{repo_name} already exists. Would you like to (o)verwrite, (s)kip, or (u)pdate? ").lower()
        if choice == 'o':
            print(f'Removing and re-cloning {repo_name}...')
            try:
                # Change directory permissions to writable, then remove it
                shutil.rmtree(repo_dir, onerror=make_writable)
                print(f'{repo_name} removed successfully.')

                # Now clone the repository again
                subprocess.run(['git', 'clone', repo_url, repo_dir])
                print(f'{repo_name} cloned successfully.')
            except Exception as e:
                print(f"Failed to remove and re-clone {repo_name}: {e}")
        elif choice == 'u':
            print(f'Pulling latest changes for {repo_name}...')
            try:
                subprocess.run(['git', '-C', repo_dir, 'pull'])
                print(f'{repo_name} updated successfully.')
            except Exception as e:
                print(f"Failed to update {repo_name}: {e}")
        else:
            print(f'Skipping {repo_name}.')
# Main script flow
use_cache = True
while True:
    # Get credentials from cache or prompt user
    GITHUB_USERNAME, GITHUB_PASSWORD = get_github_credentials(use_cache=use_cache)
    
    # Attempt authentication
    repos = authenticate_github(GITHUB_USERNAME, GITHUB_PASSWORD)
    
    if repos is not None:
        # Authentication successful, save credentials to cache
        save_github_credentials(GITHUB_USERNAME, GITHUB_PASSWORD)
        
        # Create the backup directory if it doesn't exist
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        
        # Clone or pull each repository
        for repo in repos:
            repo_name = repo['name']
            repo_url = repo['clone_url']
            clone_or_pull_repo(repo_url, repo_name)
        
        print("Backup complete!")
        break
    else:
        # Allow the user to retry or quit
        retry = input("Would you like to retry with new credentials? (yes/no): ").strip().lower()
        if retry != 'yes':
            print("Exiting...")
            break
        else:
            # Disable cache for the next attempt and re-enter credentials
            use_cache = False

input("Press Enter to exit...")  # Keeps the window open after execution
