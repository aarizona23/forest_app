from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('forest/get_forest_mask/', GetForestMaskView.as_view(), name='get_forest_mask'),
    path('forest/get_forest_indices/', GetForestIndicesView.as_view(), name='get_forest_indices'),
    path('forest/get_burned_mask/', GetBurnedMaskView.as_view(), name='get_burned_mask'),
]
