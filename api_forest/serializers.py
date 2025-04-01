from rest_framework import serializers
from .models import *
from django.db.models import F, Avg
from django.db.models.functions import Abs

class GetForestMaskSerializer(serializers.Serializer):
    forest_unique_id = serializers.CharField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        data = super().validate(data)
        try:
            forest = ForestModel.objects.get(unique_id=data['forest_unique_id'])
        except ForestModel.DoesNotExist:
            raise serializers.ValidationError("Forest not found")
        data['forest_mask'] = (
            ForestMaskModel.objects.filter(forest=forest)
            .annotate(diff=Abs(F("timestamp") - data["end_date"]))
            .order_by("diff")  # Orders by the absolute difference
            .first()  # Gets the closest match
        )
        return data

class GetForestIndiceSerializer(serializers.Serializer):
    forest_unique_id = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    indice_name = serializers.CharField(required=True)

    def validate(self, data):
        data = super().validate(data)
        try:
            forest = ForestModel.objects.get(unique_id=data['forest_unique_id'])
        except ForestModel.DoesNotExist:
            raise serializers.ValidationError("Forest not found")

        start_date = data["start_date"]
        end_date = data["end_date"]

        # Filter indices within the date range
        data['indices'] = IndicesModel.objects.filter(
            forest=forest,
            name=data["indice_name"],
            timestamp__range=(start_date, end_date)
        ).order_by("timestamp")
        return data

class GetBurnedMaskSerializer(serializers.Serializer):
    forest_unique_id = serializers.CharField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        data = super().validate(data)
        try:
            forest = ForestModel.objects.get(unique_id=data['forest_unique_id'])
        except ForestModel.DoesNotExist:
            raise serializers.ValidationError("Forest not found")
        data['burned_mask'] = (
            BurnedMaskModel.objects.filter(forest=forest)
            .annotate(diff=Abs(F("timestamp") - data["end_date"]))
            .order_by("diff")  # Orders by the absolute difference
            .first()  # Gets the closest match
        )
        return data

class GetDeforestationSerializer(serializers.Serializer):
    forest_unique_id = serializers.CharField(required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        data = super().validate(data)
        try:
            forest = ForestModel.objects.get(unique_id=data['forest_unique_id'])
        except ForestModel.DoesNotExist:
            raise serializers.ValidationError("Forest not found")

        start_date = data["start_date"]
        end_date = data["end_date"]

        # Filter forest masks
        forest_masks = ForestMaskModel.objects.filter(
            forest=forest,
            timestamp__range=(start_date, end_date)
        ).order_by("timestamp")

        forest_mask1 = forest_masks.first()
        forest_mask2 = forest_masks.last()

        if not forest_mask1 or not forest_mask2:
            raise serializers.ValidationError("Forest masks not found")

        # Calculate deforestation
        data['forest_mask1'] = forest_mask1
        data['forest_mask2'] = forest_mask2
        return data