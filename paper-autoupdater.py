import requests
import json
import os
from config import papermcVersion  # Ensure papermcVersion is a string

# PaperMC API URL
API_BASE = "https://api.papermc.io/v2/projects/paper"
INFO_FILE = "paper_info.json"
PAPER_JAR = "paper.jar"

# Load saved information
if os.path.exists(INFO_FILE):
    with open(INFO_FILE, "r") as f:
        saved_info = json.load(f)
else:
    saved_info = {}

# Get the available versions
response = requests.get(API_BASE)
data = response.json()

# Check if the selected version exists in the available versions
if papermcVersion not in data['versions']:
    print(f"Version {papermcVersion} not found.")
    exit(1)

# Get the selected version based on papermcVersion name
current_version = papermcVersion

# Get the latest build for the selected version
response = requests.get(f"{API_BASE}/versions/{current_version}")
data = response.json()
latest_build = data['builds'][-1]

# Check if the version and build are already downloaded
if saved_info.get("version") == current_version and saved_info.get("build") == latest_build:
    print(f"File paper-{current_version}-{latest_build}.jar is already downloaded.")
else:
    # Remove the old file if it exists
    if os.path.exists(PAPER_JAR):
        os.remove(PAPER_JAR)
    
    # Construct the download URL
    file_name = f"paper-{current_version}-{latest_build}.jar"
    download_url = f"{API_BASE}/versions/{current_version}/builds/{latest_build}/downloads/{file_name}"
    
    # Download the file
    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        with open(file_name, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        os.rename(file_name, PAPER_JAR)
        print(f"File {file_name} successfully downloaded and renamed to {PAPER_JAR}!")
        
        # Update the JSON file with the new version and build info
        with open(INFO_FILE, "w") as f:
            json.dump({"version": current_version, "build": latest_build}, f)
    else:
        print("Error downloading the file.")
