import os
import sys
import django
from future.backports.datetime import datetime

# Get the project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project directory to the Python path
sys.path.append(BASE_DIR)

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "forest_app.settings")  # Update this with your actual settings module
django.setup()

from api_forest.models import ForestModel, ForestMaskModel, BurnedMaskModel
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from datetime import datetime
from django.utils.timezone import make_aware

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
    forest = ForestModel.objects.get(id=1)
    for subfolder_id, subfolder_name in subfolders.items():
        if subfolder_name == "fire":
            tiff_files = get_tiff_files(service, subfolder_id)
            print(f"Found {len(tiff_files)} TIFF files in 'fire' subfolder")
            for file_id, file_name in tiff_files:
                print(file_name)
                date_str = file_name.split("_")[3]
                date_datetime = datetime.strptime(date_str, "%Y-%m-%d")
                timestamp = make_aware(date_datetime)
                BurnedMaskModel.objects.create(
                    burned_mask="https://drive.google.com/file/d/" + file_id,
                    forest=forest,
                    timestamp=timestamp
                )

    print("Script completed successfully")
