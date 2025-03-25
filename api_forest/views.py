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
        return Response(forest_mask.forest_mask)

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
        return Response(burned_mask.burned_mask)


