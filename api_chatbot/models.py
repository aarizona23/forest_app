from django.db import models
from django.contrib.auth.models import User

class MessageModel(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)