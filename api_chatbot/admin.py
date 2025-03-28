from django.contrib import admin
from .models import MessageModel

@admin.register(MessageModel)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'text', 'created_at')
    list_filter = ('role', 'user')
    search_fields = ('text',)
