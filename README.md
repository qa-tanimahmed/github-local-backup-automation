# github-local-backup-automation
python script that automatically backs up all your github repositories to the same location, where the script is stored.

This project consists of two Python scripts:
1. **`backup.py`**: A script for backing up GitHub repositories. It authenticates with GitHub, either using cached credentials or prompting the user to enter them. It can clone or update repositories in a specified directory.
2. **`clear.py`**: A script for clearing cached GitHub credentials from the keyring.

## Features
- **Backup Repositories**: Clone or update repositories from GitHub.
- **Credential Management**: Save and load GitHub credentials using the keyring library.
- **Clear Credentials**: Remove stored credentials from the keyring.

## Prerequisites
- **Python**: Version 3.6 or higher. Download from [python.org](https://www.python.org/downloads/).
- **pip**: Package installer for Python. It is included with Python 3.4 and later. Verify installation with `pip --version`.
- **Virtual Environment** (Optional but recommended): Use `venv` to create isolated environments for managing dependencies.
- **GitHub Personal Access Token (PAT)**: Required for authenticating API requests. You need to generate a PAT from your GitHub account settings with the `repo` scope.
  
## Installation
1. Clone the repository.
   
   ```
   git clone https://github.com/qa-tanimahmed/github-local-backup-automation.git
   ```
2. Navigate to the project directory.
3. Install required packages.
   
   ```
   pip install requests keyring
   ```
## Usage
1. Run the main backup script:
   
   ```
   python backup.py
   ```
2.Follow the prompts to enter your GitHub username and PAT, or use cached credentials.

## Clear Cached Credentials
1. Run the credentials clearing script:
  ```
  python clear.py
  ```
This will remove your cached GitHub credentials from the keyring.

For questions or suggestions, please reach out to tanimahmed0137@gmail.com.

   
