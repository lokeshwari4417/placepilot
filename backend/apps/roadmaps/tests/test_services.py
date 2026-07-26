import pytest
from django.utils import timezone

from apps.accounts.models import User
from apps.roadmaps.models import Roadmap, RoadmapProgress, RoadmapTopic
from apps.roadmaps.services import RoadmapService


@pytest.mark.django_db
class TestRoadmapService:
    def test_get_or_create_progress_creates_new(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test description",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        
        progress = RoadmapService.get_or_create_progress(user, roadmap)
        
        assert progress.user == user
        assert progress.roadmap == roadmap
        assert progress.status == RoadmapProgress.Status.NOT_STARTED

    def test_start_roadmap(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test description",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        
        progress = RoadmapService.start_roadmap(user, roadmap)
        
        assert progress.status == RoadmapProgress.Status.IN_PROGRESS
        assert progress.started_at is not None

    def test_complete_topic(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test description",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        topic = RoadmapTopic.objects.create(
            roadmap=roadmap,
            title="Test Topic",
            order=1
        )
        
        progress = RoadmapService.complete_topic(user, roadmap, topic)
        
        assert topic in progress.completed_topics.all()
        assert progress.completion_percentage == 100

    def test_complete_multiple_topics(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test description",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        topic1 = RoadmapTopic.objects.create(roadmap=roadmap, title="Topic 1", order=1)
        topic2 = RoadmapTopic.objects.create(roadmap=roadmap, title="Topic 2", order=2)
        
        RoadmapService.complete_topic(user, roadmap, topic1)
        progress = RoadmapService.complete_topic(user, roadmap, topic2)
        
        assert progress.completion_percentage == 100
        assert progress.status == RoadmapProgress.Status.COMPLETED

    def test_uncomplete_topic(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        roadmap = Roadmap.objects.create(
            title="Test Roadmap",
            description="Test description",
            target_role=Roadmap.TargetRole.FRONTEND
        )
        topic = RoadmapTopic.objects.create(
            roadmap=roadmap,
            title="Test Topic",
            order=1
        )
        
        RoadmapService.complete_topic(user, roadmap, topic)
        progress = RoadmapService.uncomplete_topic(user, roadmap, topic)
        
        assert topic not in progress.completed_topics.all()
        assert progress.completion_percentage == 0
