import pytest
from apps.accounts.models import User
from apps.analytics.models import ReadinessScore
from apps.analytics.services import ReadinessScoreService


@pytest.mark.django_db
class TestReadinessScoreService:
    def test_get_or_create_score_creates_new_score(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        score = ReadinessScoreService.get_or_create_score(user)
        
        assert score.user == user
        assert score.overall_score == 0
        assert score.coding_score == 0
        assert score.aptitude_score == 0
        assert score.resume_score == 0
        assert score.interview_score == 0
        assert score.roadmap_progress == 0
        assert score.streak_days == 0

    def test_get_or_create_score_returns_existing(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        existing = ReadinessScore.objects.create(
            user=user,
            overall_score=50,
            coding_score=60,
            aptitude_score=40
        )
        
        score = ReadinessScoreService.get_or_create_score(user)
        
        assert score.id == existing.id
        assert score.coding_score == 60

    def test_calculate_overall_score(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        score = ReadinessScore.objects.create(
            user=user,
            coding_score=80,
            aptitude_score=70,
            resume_score=90,
            interview_score=85
        )
        
        overall = ReadinessScoreService.calculate_overall_score(score)
        
        # Weighted: 80*0.30 + 70*0.20 + 90*0.25 + 85*0.25 = 24 + 14 + 22.5 + 21.25 = 81.75 -> 81
        assert overall == 81

    def test_update_score(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        score = ReadinessScoreService.update_score(
            user,
            coding_score=75,
            aptitude_score=60
        )
        
        assert score.coding_score == 75
        assert score.aptitude_score == 60
        assert score.overall_score == 22  # 75*0.30 + 60*0.20 = 22.5 -> 22

    def test_update_score_clamps_values(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        score = ReadinessScoreService.update_score(
            user,
            coding_score=150,  # Above 100
            aptitude_score=-50  # Below 0
        )
        
        assert score.coding_score == 100
        assert score.aptitude_score == 0
