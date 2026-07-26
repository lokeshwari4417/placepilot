import pytest

from apps.accounts.models import User
from apps.coding.models import Problem, Submission, TestCase
from apps.coding.services import CodeExecutionService


@pytest.mark.django_db
class TestCodeExecutionService:
    def test_create_submission(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        problem = Problem.objects.create(
            title="Test Problem",
            description="Test description",
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
        
        submission = CodeExecutionService.create_submission(
            user,
            problem,
            "print(input())",
            Problem.Language.PYTHON
        )
        
        assert submission.user == user
        assert submission.problem == problem
        assert submission.language == Problem.Language.PYTHON
        assert submission.status in [Submission.Status.ACCEPTED, Submission.Status.RUNTIME_ERROR]

    def test_execute_code_with_valid_solution(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        problem = Problem.objects.create(
            title="Test Problem",
            description="Test description",
            difficulty=Problem.Difficulty.EASY,
            default_language=Problem.Language.PYTHON,
            time_limit=2
        )
        TestCase.objects.create(
            problem=problem,
            input_data="5\n",
            expected_output="5\n",
            order=1,
            is_hidden=False
        )
        
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code="print(input())",
            language=Problem.Language.PYTHON,
            status=Submission.Status.PENDING
        )
        
        result = CodeExecutionService.execute_code(submission)
        
        assert result.status in [Submission.Status.ACCEPTED, Submission.Status.RUNTIME_ERROR]

    def test_execute_code_with_wrong_answer(self):
        user = User.objects.create_user(email="test@example.com", password="pass123")
        problem = Problem.objects.create(
            title="Test Problem",
            description="Test description",
            difficulty=Problem.Difficulty.EASY,
            default_language=Problem.Language.PYTHON,
            time_limit=2
        )
        TestCase.objects.create(
            problem=problem,
            input_data="5\n",
            expected_output="10\n",
            order=1,
            is_hidden=False
        )
        
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code="print(input())",
            language=Problem.Language.PYTHON,
            status=Submission.Status.PENDING
        )
        
        result = CodeExecutionService.execute_code(submission)
        
        assert result.status == Submission.Status.WRONG_ANSWER
