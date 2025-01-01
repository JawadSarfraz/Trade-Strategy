import json
import os

def load_credentials():
    """Load API credentials from configs/credentials.json."""
    # Define the path to the credentials file
    credentials_path = os.path.join(os.getcwd(), "configs", "credentials.json")
    
    try:
        # Open and load the credentials JSON file
        with open(credentials_path, "r") as file:
            credentials = json.load(file)
        return credentials
    except FileNotFoundError:
        raise FileNotFoundError("API credentials file not found. Please create configs/credentials.json.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding JSON. Ensure credentials.json is formatted correctly.")
