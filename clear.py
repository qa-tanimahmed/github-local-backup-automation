import keyring

# Constants for the GitHub service and credential keys
GITHUB_SERVICE = 'github_backup'

def clear_github_credentials():
    """Clear cached GitHub credentials from keyring."""
    try:
        # Remove cached username and password (PAT) from keyring
        if keyring.get_password(GITHUB_SERVICE, 'username') is not None:
            keyring.delete_password(GITHUB_SERVICE, 'username')
            print("Username cleared from cache.")
        else:
            print("No cached username found.")

        if keyring.get_password(GITHUB_SERVICE, 'password') is not None:
            keyring.delete_password(GITHUB_SERVICE, 'password')
            print("Password cleared from cache.")
        else:
            print("No cached password found.")
        
        print("Cached GitHub credentials have been removed successfully.")
    except keyring.errors.PasswordDeleteError as e:
        print(f"Error removing credentials: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    clear_github_credentials()
    input("Press Enter to exit...")  # Prevent the console from closing immediately
