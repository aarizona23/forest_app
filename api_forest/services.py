import concurrent.futures
import threading
import time
import os
# Google Drive API
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
from io import BytesIO
import re
from uuid import uuid4
from PIL import Image
from forest_app import settings
import numpy as np

class GetDeforestation:
    def __init__(self, urls):
        self.urls = urls

    def download_tiff(self, url):
        """Download TIFF from Google Drive using OAuth."""
        file_id = self.extract_drive_id(url)
        if not file_id:
            print(f"Invalid Google Drive URL: {url}")
            return None

        try:
            creds = Credentials.from_service_account_file("credentials.json")
            service = build("drive", "v3", credentials=creds)

            request = service.files().get_media(fileId=file_id)
            file_stream = BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)

            done = False
            while not done:
                _, done = downloader.next_chunk()

            file_stream.seek(0)
            return Image.open(file_stream)

        except Exception as e:
            print(f"Error downloading TIFF from Google Drive: {e}")
            return None

    def delete_with_delay(self, file_path, delay=600):
        """Delete file after a delay (in seconds)."""
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted file after {delay} seconds: {file_path}")

    def delete_file(self, file_path):
        threading.Thread(target=self.delete_with_delay, args=(file_path,)).start()

    def extract_drive_id(self, url):
        """Extract Google Drive File ID from URL."""
        match = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
        return match.group(1) if match else None

    def save_png_file(self, array):
        """Save the processed PNG file locally and return its path & URL."""
        temp_dir = os.path.join(settings.MEDIA_ROOT, "forest_masks_temp")
        os.makedirs(temp_dir, exist_ok=True)

        file_name = f"{uuid4()}.png"
        file_path = os.path.join(temp_dir, file_name)

        # Convert array to image and save as PNG
        Image.fromarray(array).save(file_path, format="PNG")

        # Generate URL for accessing the file
        file_url = f"{settings.MEDIA_URL}forest_masks_temp/{file_name}"

        return file_path, file_url

    def execute(self):
        # Parallel Download of TIFF Images
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(self.download_tiff, self.urls))

        if any(r is None for r in results):
            return None

        img1, img2 = results

        # Convert to NumPy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Optimized Logical Operation using np.maximum
        result_arr = np.maximum(arr1, arr2).astype(np.uint8) * 255  # Convert to 255 for visualization

        # Save to PNG and get file path
        file_path, file_url = self.save_png_file(result_arr)

        # Delete files
        self.delete_file(file_path)

        return file_url