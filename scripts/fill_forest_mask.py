import os
import numpy as np
import rasterio
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from io import BytesIO

CREDENTIALS_FILE = "credentials.json"
FOLDER_ID = "ВАШ_ИДЕНТИФИКАТОР_ПАПКИ"


def authenticate_google_drive(self):
    """ Authenticate and return Google Drive API service instance """
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive"]
    )
    return build("drive", "v3", credentials=credentials)


def get_drive_files(self, service):
    """ Retrieve a list of TIFF files from the specified Google Drive folder """
    query = f"'{FOLDER_ID}' in parents and mimeType='image/tiff'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return {file["id"]: file["name"] for file in results.get("files", [])}


def process_tif_file(self, service, file_id, file_name):
    """ Download a TIFF file, convert its mask to an array """
    request = service.files().get_media(fileId=file_id)
    file_stream = BytesIO()
    downloader = MediaIoBaseDownload(file_stream, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    file_stream.seek(0)
    with rasterio.open(file_stream) as src:
        img = src.read(1)  # Read the first (and usually only) band

    # Convert mask values:
    # - 255 becomes 1 (forest)
    # - 100 becomes 2 (cloud/water)
    # - 0 remains 0
    new_img = np.copy(img)
    new_img[img == 255] = 1
    new_img[img == 100] = 2
    return new_img


def save_to_db(self, file_name, arr_mask):
    """ Save the processed mask array to the database """
    from api_forest.models import ForestMaskModel  # Import the model

    mask_instance = ForestMaskModel(
        file_name=file_name,
        mask_data=arr_mask.tolist()  # Convert the array to a JSON-compatible list
    )
    mask_instance.save()

if __name__ == "__main__":
    service = authenticate_google_drive()
    files = get_drive_files(service)
    for file_id, file_name in files.items():
        mask_array = process_tif_file(service, file_id, file_name)
        save_to_db(file_name, mask_array)