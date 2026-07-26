import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.coding.models import Problem, Submission, TestCase


@pytest.mark.django_db
class TestProblemViewSet:
    def test_list_problems_requires_auth(self):
        client = APIClient()
        response = client.get(reverse("problem-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_problems_authenticated(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        Problem.objects.create(
            title="Test Problem",
            description="Test",
            difficulty=Problem.Difficulty.EASY
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("problem-list"))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


@pytest.mark.django_db
class TestSubmissionListView:
    def test_list_submissions_requires_auth(self):
        client = APIClient()
        response = client.get(reverse("coding:submission-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_user_submissions(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        problem = Problem.objects.create(
            title="Test Problem",
            description="Test",
            difficulty=Problem.Difficulty.EASY
        )
        Submission.objects.create(
            user=user,
            problem=problem,
            code="print('test')",
            language=Problem.Language.PYTHON,
            status=Submission.Status.ACCEPTED
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get(reverse("coding:submission-list"))
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_submit_solution(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        problem = Problem.objects.create(
            title="Test Problem",
            description="Test",
            difficulty=Problem.Difficulty.EASY,
            default_language=Problem.Language.PYTHON
        )
        TestCase.objects.create(
            problem=problem,
            input_data="5\n",
            expected_output="5\n",
            order=1,
            is_hidden=False
        )
        
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            reverse("coding:problem-submit", kwargs={"problem_id": problem.id}),
            {"code": "print(input())", "language": "python"}
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert "status" in response.data
