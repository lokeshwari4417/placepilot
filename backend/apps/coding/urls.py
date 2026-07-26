from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProblemViewSet, SubmissionDetailView, SubmissionListView

router = DefaultRouter()
router.register(r"problems", ProblemViewSet, basename="problem")

urlpatterns = [
    path("submissions/", SubmissionListView.as_view(), name="submission-list"),
    path("submissions/<uuid:pk>/", SubmissionDetailView.as_view(), name="submission-detail"),
    path("problems/<uuid:problem_id>/submit/", SubmissionListView.as_view(), name="problem-submit"),
] + router.urls
