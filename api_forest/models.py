from django.db import models
from django.db.models import TextChoices

# Create your models here.
class IndicesTypes(TextChoices):
    NDVI = 'NDVI'
    NDWI = 'NDWI'
    EVI = 'EVI'
    NBR = 'NBR'
    SAVI = 'SAVI'
    GNDVI = 'GNDVI'
    SIPI = 'SIPI'
    MGRVI = 'MGRVI'
    TGI = 'TGI'
    VARI = 'VARI'
    GRVI = 'GRVI'
    SR = 'SR'
    CI = 'CI'
    MSR = 'MSR'
    OSAVI = 'OSAVI'
    NDMI = 'NDMI'
    MSAVI = 'MSAVI'
    NDRI = 'NDRI'
    RECI = 'RECI'

class ForestModel(models.Model):
    name = models.CharField(max_length=250)
    polygon_coors = models.JSONField()
    description = models.TextField(blank=True, null=True)

class IndicesModel(models.Model):
    name = models.CharField(max_length=250, choices=IndicesTypes.choices)
    value = models.FloatField()
    forest = models.ForeignKey(ForestModel, on_delete=models.CASCADE, related_name='indices')
    timestamp = models.DateTimeField()

class ForestMaskModel(models.Model):
    forest = models.ForeignKey(ForestModel, on_delete=models.CASCADE, related_name='classification')
    forest_mask = models.JSONField()
    timestamp = models.DateTimeField()