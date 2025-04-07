from django.urls import path
from .views import ChatbotAPIView, ChatHistoryAPIView

urlpatterns = [
    path('chat/', ChatbotAPIView.as_view()),
    path('chat/history/', ChatHistoryAPIView.as_view()),
]