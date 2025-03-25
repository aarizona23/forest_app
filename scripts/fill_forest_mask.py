import os
import sys
import django
import numpy as np
import rasterio
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from io import BytesIO
from datetime import datetime
from django.utils.timezone import make_aware

# Get the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project directory to the Python path
sys.path.append(BASE_DIR)

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forest_app.settings")  # Update this with your actual settings module
django.setup()

from api_forest.models import ForestModel, ForestMaskModel

CREDENTIALS_FILE = "credentials.json"
MAIN_FOLDER_ID = "1COBgLF6MQTJXzXqJRkUeJw22kEqsXJ0f"


def authenticate_google_drive():
    """ Authenticate and return Google Drive API service instance """
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)


def get_subfolders(service, parent_folder_id):
    """ Retrieve subfolder IDs inside the parent folder """
    query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return {folder["id"]: folder["name"] for folder in results.get("files", [])}


def get_forest_folder(service, subfolder_id):
    """ Retrieve the 'forest' folder inside a subfolder """
    query = f"'{subfolder_id}' in parents and name='forest' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    # Get the list of files found
    folders = results.get("files", [])

    if not folders:  # If the list is empty, return None
        print(f"No 'forest' folder found in subfolder ID: {subfolder_id}")
        return None

    return folders[0]["id"]  # Return the first matching folder ID


def get_satellite_folders(service, forest_folder_id):
    """ Retrieve 'sentinel' and 'landsat' folders inside 'forest' folder """
    query = f"'{forest_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return {folder["id"]: folder["name"] for folder in results.get("files", [])}


def extract_forest_info(file_name):
    """ Extract unique_id and timestamp from file name """
    print(file_name)
    file_name = file_name.replace(".tif", "")
    parts = file_name.split("_")
    print(parts)
    unique_id = parts[0]
    print(unique_id)
    try:
        last_part = parts[-1]
        if 'mask' in last_part:
            date_str = last_part.replace("mask", "")
        else:
            date_str = last_part
        timestamp = datetime.strptime(date_str, "%Y-%m-%d")
        timestamp = make_aware(timestamp)
    except ValueError:
        return unique_id, None
    print(timestamp)
    return unique_id, timestamp


def save_to_db(file_name, file_id):
    """ Save the processed mask array to the database """
    print(f"Processing {file_name}")
    unique_id, timestamp = extract_forest_info(file_name)
    if not unique_id or not timestamp:
        print(f"Skipping {file_name} due to invalid format")
        return

    forest, _ = ForestModel.objects.get_or_create(unique_id=unique_id, defaults={"name": unique_id})
    ForestMaskModel.objects.get_or_create(
        forest=forest,
        forest_mask="https://drive.google.com/file/d/" + file_id,
        timestamp=timestamp
    )

def get_tiff_files(service, folder_id):
    """ Retrieve TIFF files inside a folder """
    query = f"'{folder_id}' in parents and mimeType='image/tiff'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return [(file["id"], file["name"]) for file in results.get("files", [])]


if __name__ == "__main__":
    service = authenticate_google_drive()
    print("Authenticated successfully")
    subfolders = get_subfolders(service, MAIN_FOLDER_ID)
    print(f"Found {len(subfolders)} subfolders")

    for subfolder_id, subfolder_name in subfolders.items():
        forest_folder_id = get_forest_folder(service, subfolder_id)
        if not forest_folder_id:
            print(f"No 'forest' folder found in {subfolder_name}")
            continue

        satellite_folders = get_satellite_folders(service, forest_folder_id)
        for sat_folder_id, sat_folder_name in satellite_folders.items():
            print(f"Processing {sat_folder_name} folder")
            tiff_files = get_tiff_files(service, sat_folder_id)
            print(f"Processing {len(tiff_files)} TIFF files from {sat_folder_name} folder")
            for file_id, file_name in tiff_files:
                print(f"Processing {file_name}") # Pass file object
                save_to_db(file_name, file_id)