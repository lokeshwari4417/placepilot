from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CompleteTopicView,
    RoadmapProgressDetailView,
    RoadmapProgressListView,
    RoadmapViewSet,
    UncompleteTopicView,
)

router = DefaultRouter()
router.register(r"", RoadmapViewSet, basename="roadmap")

urlpatterns = [
    path("progress/", RoadmapProgressListView.as_view(), name="progress-list"),
    path("progress/<uuid:roadmap_id>/", RoadmapProgressDetailView.as_view(), name="progress-detail"),
    path("progress/<uuid:roadmap_id>/complete/", CompleteTopicView.as_view(), name="complete-topic"),
    path("progress/<uuid:roadmap_id>/uncomplete/", UncompleteTopicView.as_view(), name="uncomplete-topic"),
] + router.urls
