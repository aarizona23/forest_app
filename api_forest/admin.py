from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(ForestModel)
class ForestModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(IndicesModel)
class IndicesModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'forest', 'timestamp')

@admin.register(ForestMaskModel)
class ForestClassificationModelAdmin(admin.ModelAdmin):
    list_display = ('forest', 'timestamp')

@admin.register(BurnedMaskModel)
class BurnedMaskModelAdmin(admin.ModelAdmin):
    list_display = ('forest', 'timestamp')