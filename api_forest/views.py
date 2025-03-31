from django.contrib.admin.templatetags.admin_list import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
import numpy as np
from .serializers import *

class CustomPagination(PageNumberPagination):
    def __init__(self, page_size=None):
        self.page_size = page_size

class GetForestMaskView(APIView):
    def post(self, request):
        serializer = GetForestMaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forest_mask = serializer.validated_data['forest_mask']
        return Response(forest_mask.forest_mask.url if forest_mask else None)

class GetForestIndicesView(APIView):
    def post(self, request):
        serializer = GetForestIndiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        indices = serializer.validated_data['indices']

        # Get the total count
        count = indices.count()

        if count <= 12:
            indice_values = list(indices.values_list("value"))
            indice_values_list = [i[0] for i in indice_values]
            return Response(indice_values_list) # Return raw data if 12 or fewer

        # If more than 12, group and average
        grouped_indices = []
        timestamps = np.linspace(0, count - 1, 12, dtype=int)  # 12 evenly spaced indices

        for i in range(len(timestamps) - 1):
            start_idx = timestamps[i]
            end_idx = timestamps[i + 1]

            avg_values = indices[start_idx:end_idx].aggregate(
                mean_value=Avg("value")  # Replace "value" with your actual field
            )

            if avg_values["mean_value"] is not None:
                grouped_indices.append(
                    avg_values["mean_value"]
                )

        return Response(grouped_indices)

class GetBurnedMaskView(APIView):
    def post(self, request):
        serializer = GetBurnedMaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        burned_mask = serializer.validated_data['burned_mask']
        return Response(burned_mask.burned_mask.url if burned_mask else None)

class GetDeforestationView(APIView):
    def post(self, request):
        serializer = GetDeforestationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        forest_mask1 = serializer.validated_data['forest_mask1']
        forest_mask2 = serializer.validated_data['forest_mask2']
        pass
        """
        if img1 is None or img2 is None:
            return Response({"error": "Failed to download one or both TIFF files"}, status=status.HTTP_400_BAD_REQUEST)

            # Convert to NumPy arrays
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Apply comparison logic: (arr1 & 1) | (arr2 & 1)
        result_arr = ((arr1 & 1) | (arr2 & 1)).astype(np.uint8) * 255  # Scale 1 → 255 for visibility

        # Convert back to TIFF
        result_tiff = self.create_tiff(result_arr)

        # Return image as response
        return self.send_image_response(result_tiff)

    def download_tiff(self, url):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
            return Image.open(BytesIO(response.content))
        except Exception as e:
            print(f"Error downloading TIFF from {url}: {e}")
            return None

    def create_tiff(self, array):
        img = Image.fromarray(array)
        output = BytesIO()
        img.save(output, format="TIFF")
        output.seek(0)
        return output

    def send_image_response(self, image):
        response = Response(image.getvalue(), content_type="image/tiff")
        response["Content-Disposition"] = "attachment; filename=deforestation_mask.tiff"
        return response
        """


