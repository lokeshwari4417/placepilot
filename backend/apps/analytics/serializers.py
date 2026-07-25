from rest_framework import serializers

from .models import ReadinessScore


class ReadinessScoreSerializer(serializers.ModelSerializer):
    """Serializer for ReadinessScore model."""
    
    class Meta:
        model = ReadinessScore
        fields = [
            "id",
            "overall_score",
            "coding_score",
            "aptitude_score",
            "resume_score",
            "interview_score",
            "roadmap_progress",
            "streak_days",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
