from django.urls import path

from .views import ReadinessScoreView

app_name = "analytics"

urlpatterns = [
    path("readiness-score/", ReadinessScoreView.as_view(), name="readiness-score"),
]
