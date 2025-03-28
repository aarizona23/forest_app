from rest_framework import serializers
from .models import MessageModel

class ChatbotMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageModel
        fields = ['role', 'text', 'created_at']