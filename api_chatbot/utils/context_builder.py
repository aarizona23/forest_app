from rest_framework.test import APIRequestFactory
from api_forest.views import GetForestIndicesView, GetBurnedMaskView, GetDeforestationView
from api_forest.models import ForestModel, IndicesModel
from datetime import datetime

from django.db.models import Avg
import numpy as np

def get_index_summary(parsed: dict) -> str:
    forest_id = parsed.get("forest_id")
    index = parsed.get("index")
    start_date = parsed.get("start_date")
    end_date = parsed.get("end_date")

    if not forest_id or not index or not start_date or not end_date:
        return f"Invalid input. Forest ID or Indice Name is missing."

    try:
        forest = ForestModel.objects.get(id=forest_id)
    except ForestModel.DoesNotExist:
        return f"No data found for forest ID {forest_id}"

    entries = IndicesModel.objects.filter(
        forest=forest,
        name=index,
        timestamp__range=[start_date, end_date]
    ).order_by("timestamp")

    count = entries.count()

    print("Check count of indeces: ", count)
    
    if count == 0:
        return f"No {index} data found for forest ID {forest_id} between {start_date} and {end_date}"

    # If 12 or fewer, return raw data
    if count <= 12:
        indice_values = list(entries.values_list("value", flat=True))
        summary = f"{index} values for forest ID {forest_id}:\n"
        for value in indice_values:
            summary += f"• {value:.2f}\n"
        return summary

    # If more than 12, group and average
    grouped_indices = []
    timestamps = np.linspace(0, count - 1, 12, dtype=int)  # Generate 12 evenly spaced indices

    for i in range(len(timestamps) - 1):
        start_idx = timestamps[i]
        end_idx = timestamps[i + 1]

        avg_values = entries[start_idx:end_idx].aggregate(mean_value=Avg("value"))

        if avg_values["mean_value"] is not None:
            grouped_indices.append(avg_values["mean_value"])

    # Format output
    summary = f"{index} averaged values for forest ID {forest_id}:\n"
    for value in grouped_indices:
        summary += f"• {value:.2f}\n"

    return summary


def get_burned_area_summary(parsed: dict) -> str:
    data = {
        "forest_id": parsed.get("forest_id"),
        "end_date": parsed.get("end_date")
    }

    factory = APIRequestFactory()
    request = factory.post('/forest/get_burned_mask/', data, format='json')
    
    view = GetBurnedMaskView.as_view()
    response = view(request)

    if response.status_code == 200:
        return f"Burned area mask URL: {response.data}"
    else:
        return "No relevant burned area data found."

def get_deforestation_summary(parsed: dict) -> str:
    data = {
        "forest_id": parsed.get("forest_id"),
        "start_date": parsed.get("start_date"),
        "end_date": parsed.get("end_date")
    }

    factory = APIRequestFactory()
    request = factory.post('/forest/get_deforestation/', data, format='json')
    
    view = GetDeforestationView.as_view()
    response = view(request)

    if response.status_code == 200:
        return f"Deforestation analysis result: {response.data}"
    else:
        return "No relevant deforestation data found."