import os
import numpy as np
from PIL import Image
from rest_framework.test import APIRequestFactory
from api_forest.models import ForestModel, IndicesModel
from api_forest.views import GetBurnedMaskView, GetDeforestationMaskView

def get_index_summary(parsed: dict) -> str:
    forest_unique_id = parsed.get("forest_unique_id")
    index = parsed.get("index")
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    if not forest_unique_id or not index or not start_date or not end_date:
        return f"Invalid input. Forest ID or Indice Name is missing."

    try:
        forest = ForestModel.objects.get(unique_id=forest_unique_id)
    except ForestModel.DoesNotExist:
        return f"No data found for forest ID {forest_unique_id}"

    entries = IndicesModel.objects.filter(
        forest=forest,
        name=index,
        timestamp__range=[start_date, end_date]
    ).order_by("timestamp")

    count = entries.count()

    print("Check count of indeces: ", count)
    
    if count == 0:
        return f"No {index} data found for forest ID {forest_unique_id} between {start_date} and {end_date}"

    # If 12 or fewer, return raw data with dates
    if count <= 12:
        indice_values = list(entries.values_list("value", "timestamp"))
        summary = f"{index} values for forest ID {forest_unique_id}:\n"
        for value, timestamp in indice_values:
            summary += f"• {value:.2f} ({timestamp.date()})\n"
        return summary

    # If more than 12, group and average
    grouped_indices = []
    date_ranges = []
    timestamps = np.linspace(0, count - 1, 12, dtype=int)  # Generate 12 evenly spaced indices

    for i in range(len(timestamps) - 1):
        start_idx = timestamps[i]
        end_idx = timestamps[i + 1]

        # Get the subset of entries for the current range (as a list)
        sub_entries = list(entries[start_idx:end_idx])

        if len(sub_entries) == 0:
            continue

        avg_values = (
            sum(entry.value for entry in sub_entries) / len(sub_entries)
        )  # Calculate the average manually

        grouped_indices.append(avg_values)

        # Add the date range for the current group using list indexing
        date_start = sub_entries[0].timestamp.date()  # First entry in the slice
        date_end = sub_entries[-1].timestamp.date()   # Last entry in the slice
        date_ranges.append((date_start, date_end))

    # Format output
    summary = f"{index} averaged values for forest ID {forest_unique_id} with dates:\n"
    for value, date_range in zip(grouped_indices, date_ranges):
        summary += f"• {value:.2f} ({date_range[0]} - {date_range[1]})\n"

    return summary

# Assuming the file is stored in your repo under FOREST_APP/files/
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))

def analyze_burned_mask(image_path: str) -> str:
    """
    Analyze the burned area mask image and extract relevant statistics.
    Optimized to handle high-resolution images efficiently.
    """
    try:
        with Image.open(image_path) as img:
            # Optionally resize the image for faster processing (e.g., downscale by a factor of 4)
            img = img.resize((img.width // 4, img.height // 4))
            img = img.convert('L')  # Convert to grayscale

            img_array = np.array(img)

            # Burned pixels are anything that is NOT pure black (0)
            burned_pixels = np.sum(img_array > 0)
            total_pixels = img_array.size
            burned_percentage = (burned_pixels / total_pixels) * 100

            # Additional statistics
            min_intensity = np.min(img_array)
            max_intensity = np.max(img_array)
            mean_intensity = np.mean(img_array)

            # Splitting the image into 9 sectors
            height, width = img_array.shape
            thirds_h = height // 3
            thirds_w = width // 3

            sectors = {
                "North-West": img_array[:thirds_h, :thirds_w],
                "North": img_array[:thirds_h, thirds_w:2*thirds_w],
                "North-East": img_array[:thirds_h, 2*thirds_w:],
                "West": img_array[thirds_h:2*thirds_h, :thirds_w],
                "Center": img_array[thirds_h:2*thirds_h, thirds_w:2*thirds_w],
                "East": img_array[thirds_h:2*thirds_h, 2*thirds_w:],
                "South-West": img_array[2*thirds_h:, :thirds_w],
                "South": img_array[2*thirds_h:, thirds_w:2*thirds_w],
                "South-East": img_array[2*thirds_h:, 2*thirds_w:]
            }

            sector_burned_percentages = {}

            for name, sector in sectors.items():
                sector_total = sector.size
                sector_burned = np.sum(sector > 0)
                sector_burned_percentage = (sector_burned / sector_total) * 100
                sector_burned_percentages[name] = sector_burned_percentage

            # Find the most burned sectors
            most_burned = sorted(sector_burned_percentages.items(), key=lambda x: x[1], reverse=True)[:3]
            most_burned_str = ', '.join([f"{name} ({percent:.2f}%)" for name, percent in most_burned])

            return (f"Burned area analysis: {burned_percentage:.2f}% of the total area is burned.\n"
                    f"Additional Statistics:\n"
                    f"- Minimum Intensity: {min_intensity}\n"
                    f"- Maximum Intensity: {max_intensity}\n"
                    f"- Mean Intensity: {mean_intensity:.2f}\n"
                    f"Most burned sectors: {most_burned_str}\n")
    except Exception as e:
        return f"Analysis failed: {e}"
    

def get_burned_area_summary(parsed: dict) -> str:
    data = {
        "forest_unique_id": parsed.get("forest_unique_id"),
        "end_date": parsed.get("end_date")
    }

    print(f"For burned index summary got: {data}")

    factory = APIRequestFactory()
    request = factory.post('/forest/get_burned_mask/', data, format='json')
    
    view = GetBurnedMaskView.as_view()
    response = view(request)

    if response.status_code == 200:
        # Get the URL and build the absolute path
        image_url = response.data

        if not image_url:
            return "No relevant burned area data found for the requested forest and date."

        image_path = os.path.join(BASE_DIR, image_url.strip("/"))  # This constructs the absolute path
        print(image_path)
        if os.path.exists(image_path):
            print(f"Image found at: {image_path}")
            analysis = analyze_burned_mask(image_path)
            return f"Burned area mask URL: {image_url}\n{analysis}"
        else:
            return f"Burned area mask URL: {image_url}\nAnalysis failed: Image file not found."
    else:
        return "No relevant burned area data found."

def analyze_deforestation_mask(image_path: str) -> str:
    """
    Analyze the deforestation mask image and extract relevant statistics.
    Optimized to handle high-resolution images efficiently.
    """
    try:
        with Image.open(image_path) as img:
            # Optionally resize the image for faster processing (e.g., downscale by a factor of 4)
            img = img.resize((img.width // 4, img.height // 4))
            img = img.convert('L')  # Convert to grayscale

            img_array = np.array(img)

            # Apply thresholding to remove noise
            threshold = 50 
            deforested_pixels = np.sum(img_array >= threshold)
            total_pixels = img_array.size
            deforested_percentage = (deforested_pixels / total_pixels) * 100

            # Divide image into 9 sectors
            height, width = img_array.shape
            thirds_h = height // 3
            thirds_w = width // 3

            sectors = {
                "North-West": img_array[:thirds_h, :thirds_w],
                "North": img_array[:thirds_h, thirds_w:2*thirds_w],
                "North-East": img_array[:thirds_h, 2*thirds_w:],
                "West": img_array[thirds_h:2*thirds_h, :thirds_w],
                "Center": img_array[thirds_h:2*thirds_h, thirds_w:2*thirds_w],
                "East": img_array[thirds_h:2*thirds_h, 2*thirds_w:],
                "South-West": img_array[2*thirds_h:, :thirds_w],
                "South": img_array[2*thirds_h:, thirds_w:2*thirds_w],
                "South-East": img_array[2*thirds_h:, 2*thirds_w:]
            }

            deforested_sectors = {}
            for name, sector in sectors.items():
                sector_d_pixels = np.sum(sector >= threshold)
                sector_total_pixels = sector.size
                sector_percentage = (sector_d_pixels / sector_total_pixels) * 100
                deforested_sectors[name] = sector_percentage

            sector_analysis = "\n".join([f"- {name}: {percent:.2f}% deforested" for name, percent in deforested_sectors.items()])

            return (
                f"Deforestation Analysis:\n"
                f"Total deforested area: {deforested_percentage:.2f}% of the total area.\n"
                f"Sectors Analysis:\n{sector_analysis}"
            )
    except Exception as e:
        return f"Analysis failed: {e}"

def get_deforestation_summary(parsed: dict) -> str:
    data = {
        "forest_unique_id": parsed.get("forest_unique_id"),
        "start_date": parsed.get("start_date"),
        "end_date": parsed.get("end_date")
    }

    factory = APIRequestFactory()
    request = factory.post('/forest/get_deforestation/', data, format='json')
    
    view = GetDeforestationMaskView.as_view()
    response = view(request)

    if response.status_code == 200:
        # Get the URL and build the absolute path
        image_url = response.data
        image_path = os.path.join(BASE_DIR, image_url.strip("/"))  # This constructs the absolute path

        if os.path.exists(image_path):
            analysis = analyze_deforestation_mask(image_path)
            return f"Start Date {parsed.get("start_date")} and End Date {parsed.get("end_date")} for {parsed.get("forest_unique_id")}\n Deforestation mask URL: {image_url}\n{analysis}"
        else:
            return f"Deforestation mask URL: {image_url}\nAnalysis failed: Image file not found."
    else:
        return "No relevant deforestation data found."