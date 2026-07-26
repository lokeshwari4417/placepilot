from django.db import models

from apps.core.models import BaseModel


class Problem(BaseModel):
    """Coding problem with description and constraints."""
    
    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MEDIUM = "medium", "Medium"
        HARD = "hard", "Hard"
    
    class Language(models.TextChoices):
        PYTHON = "python", "Python"
        JAVASCRIPT = "javascript", "JavaScript"
        JAVA = "java", "Java"
        CPP = "cpp", "C++"
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.EASY)
    default_language = models.CharField(max_length=20, choices=Language.choices, default=Language.PYTHON)
    time_limit = models.IntegerField(default=1)  # seconds
    memory_limit = models.IntegerField(default=256)  # MB
    tags = models.JSONField(default=list, blank=True)  # e.g., ["arrays", "dynamic-programming"]
    
    class Meta:
        ordering = ["difficulty", "title"]
    
    def __str__(self):
        return self.title


class TestCase(BaseModel):
    """Test case for a coding problem."""
    
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="test_cases")
    input_data = models.TextField()
    expected_output = models.TextField()
    is_hidden = models.BooleanField(default=True)  # Hidden test cases not shown to users
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ["problem", "order"]
        unique_together = [["problem", "order"]]
    
    def __str__(self):
        return f"{self.problem.title} - Test {self.order}"


class Submission(BaseModel):
    """Code submission for a problem."""
    
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        ACCEPTED = "accepted", "Accepted"
        WRONG_ANSWER = "wrong_answer", "Wrong Answer"
        TIME_LIMIT_EXCEEDED = "tle", "Time Limit Exceeded"
        MEMORY_LIMIT_EXCEEDED = "mle", "Memory Limit Exceeded"
        RUNTIME_ERROR = "runtime_error", "Runtime Error"
        COMPILATION_ERROR = "compilation_error", "Compilation Error"
    
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="submissions")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="submissions")
    code = models.TextField()
    language = models.CharField(max_length=20, choices=Problem.Language.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    runtime_ms = models.IntegerField(null=True, blank=True)  # Execution time in milliseconds
    memory_kb = models.IntegerField(null=True, blank=True)  # Memory usage in KB
    passed_test_cases = models.IntegerField(default=0)
    total_test_cases = models.IntegerField(default=0)
    error_message = models.TextField(blank=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.user.email} - {self.problem.title} ({self.status})"
