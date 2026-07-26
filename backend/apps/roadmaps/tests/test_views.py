import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.roadmaps.models import Roadmap, RoadmapProgress, RoadmapTopic


@pytest.mark.django_db
class TestRoadmapViewSet:
    def test_list_roadmaps_requires_auth(self):
        client = APIClient()
        response = client.get(reverse("roadmap-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_roadmaps_authenticated(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        Roadmap.objects.create(
            title="Test Roadmap",
            description="Test",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("roadmap-list"))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestRoadmapProgressListView:
    def test_list_progress_requires_auth(self):
        client = APIClient()
        response = client.get(reverse("roadmaps:progress-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_user_progress(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        RoadmapProgress.objects.create(
            user=user,
            roadmap=roadmap,
            status=RoadmapProgress.Status.IN_PROGRESS
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("roadmaps:progress-list"))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_start_roadmap(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse("roadmaps:progress-list"),
            {"roadmap_id": str(roadmap.id)}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == RoadmapProgress.Status.IN_PROGRESS


@pytest.mark.django_db
class TestCompleteTopicView:
    def test_complete_topic_requires_auth(self):
        client = APIClient()
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        response = client.post(
            reverse("roadmaps:complete-topic", kwargs={"roadmap_id": roadmap.id}),
            {"topic_id": "some-id"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_complete_topic(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        topic = RoadmapTopic.objects.create(
            roadmap=roadmap,
            title="Test Topic",
            order=1
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse("roadmaps:complete-topic", kwargs={"roadmap_id": roadmap.id}),
            {"topic_id": str(topic.id)}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["completed_topics"]) == 1
