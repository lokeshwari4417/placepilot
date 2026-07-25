import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User


@pytest.mark.django_db
class TestRegistration:
    def test_register_creates_user(self):
        client = APIClient()
        response = client.post(reverse("auth-register"), {
            "email": "student@example.com",
            "password": "StrongPass123!",
            "role": "student",
        })
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="student@example.com").exists()

    def test_cannot_self_register_as_admin(self):
        client = APIClient()
        response = client.post(reverse("auth-register"), {
            "email": "hacker@example.com",
            "password": "StrongPass123!",
            "role": "admin",
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestLogin:
    def test_login_returns_token_pair(self):
        User.objects.create_user(email="student@example.com", password="StrongPass123!")
        client = APIClient()
        response = client.post(reverse("auth-login"), {
            "email": "student@example.com",
            "password": "StrongPass123!",
        })
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data and "refresh" in response.data

    def test_me_requires_auth(self):
        client = APIClient()
        response = client.get(reverse("auth-me"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
