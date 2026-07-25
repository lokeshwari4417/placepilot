import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.analytics.models import ReadinessScore


@pytest.mark.django_db
class TestReadinessScoreView:
    def test_requires_authentication(self):
        client = APIClient()
        response = client.get(reverse("analytics:readiness-score"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_user_score(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        score = ReadinessScore.objects.create(
            user=user,
            overall_score=75,
            coding_score=80,
            aptitude_score=70
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("analytics:readiness-score"))
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == str(score.id)
        assert response.data["overall_score"] == 75
        assert response.data["coding_score"] == 80

    def test_creates_default_score_if_not_exists(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("analytics:readiness-score"))
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data["overall_score"] == 0
        assert response.data["coding_score"] == 0
        assert ReadinessScore.objects.filter(user=user).exists()
