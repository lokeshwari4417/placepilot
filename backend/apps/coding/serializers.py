from rest_framework import serializers

from .models import Problem, Submission, TestCase


class TestCaseSerializer(serializers.ModelSerializer):
    """Serializer for TestCase model (hidden test cases excluded for non-admin)."""
    
    class Meta:
        model = TestCase
        fields = ["id", "input_data", "expected_output", "order"]
        read_only_fields = ["id"]


class ProblemSerializer(serializers.ModelSerializer):
    """Serializer for Problem model."""
    
    test_cases = TestCaseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Problem
        fields = [
            "id",
            "title",
            "description",
            "difficulty",
            "default_language",
            "time_limit",
            "memory_limit",
            "tags",
            "test_cases",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Submission model."""
    
    problem = ProblemSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            "id",
            "problem",
            "code",
            "language",
            "status",
            "runtime_ms",
            "memory_kb",
            "passed_test_cases",
            "total_test_cases",
            "error_message",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class SubmissionCreateSerializer(serializers.Serializer):
    """Serializer for creating a submission."""
    
    code = serializers.CharField()
    language = serializers.ChoiceField(choices=Problem.Language.choices)
