from django.urls import path

from .views import AIAssistView

app_name = "ai_assistant"

urlpatterns = [
    path("assist/", AIAssistView.as_view(), name="ai-assist"),
]
