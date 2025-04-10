import os
import sys
import django

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
from io import BytesIO
from django.utils.timezone import make_aware
from PIL import Image
import io

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
    """Retrieve TIFF files from Google Drive as file-like objects"""
    query = f"'{folder_id}' in parents and mimeType='image/tiff'"
    results = service.files().list(q=query, fields="files(id, name)").execute()

    file_objects = []
    for file in results.get("files", []):
        file_id = file["id"]
        file_name = file["name"]
        print(f"Downloading {file_name}")
        request = service.files().get_media(fileId=file_id)
        file_stream = BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            _, done = downloader.next_chunk()

        file_stream.seek(0)  # Reset stream position for reading
        file_objects.append((file_name, file_stream))
    return file_objects

import numpy as np
def convert_tiff_to_image(file_stream, output_format="PNG"):
    """
    Converts a TIFF file stream to an image format (PNG or JPEG).
    """

    # Open the TIFF image from file stream
    image = Image.open(file_stream)

    # Convert to NumPy array
    arr = np.array(image)

    # Apply your condition — here: where pixel == 255
    mask = (arr == 255).astype(np.uint8)

    # Create an RGBA array
    height, width = mask.shape
    color_arr = np.zeros((height, width, 4), dtype=np.uint8)

    # Apply red color with full opacity where condition is met
    color_arr[mask == 1] = [139, 0, 0, 255]

    # Convert to a PIL image
    result_img = Image.fromarray(color_arr, mode="RGBA")

    # Save to in-memory buffer
    output_buffer = io.BytesIO()
    result_img.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return output_buffer

from django.core.files.base import ContentFile

if __name__ == "__main__":
    service = authenticate_google_drive()
    print("Authenticated successfully")
    subfolders = get_subfolders(service, MAIN_FOLDER_ID)
    print(f"Found {len(subfolders)} subfolders")
    forest = ForestModel.objects.get(unique_id="SemeyOrmany")
    for subfolder_id, subfolder_name in subfolders.items():
        if subfolder_name == "fire":
            tiff_files = get_tiff_files(service, subfolder_id)
            print(f"Found {len(tiff_files)} TIFF files in 'fire' subfolder")
            for file_name, file_object in tiff_files:
                date_str = file_name.split("_")[3]
                date_datetime = datetime.strptime(date_str, "%Y-%m-%d")
                timestamp = make_aware(date_datetime)
                file_image = convert_tiff_to_image(file_object)
                image_file = ContentFile(file_image.getvalue(), name=f"{file_name}.png")
                BurnedMaskModel.objects.create(
                    burned_mask=image_file,
                    forest=forest,
                    timestamp=timestamp
                )

    print("Script completed successfully")
