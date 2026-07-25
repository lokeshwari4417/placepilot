import uuid

from django.db import models

from apps.core.models import BaseModel


class ReadinessScore(BaseModel):
    """Aggregated readiness score for a student across all preparation areas."""
    
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="readiness_score"
    )
    overall_score = models.IntegerField(default=0)  # 0-100
    coding_score = models.IntegerField(default=0)  # 0-100
    aptitude_score = models.IntegerField(default=0)  # 0-100
    resume_score = models.IntegerField(default=0)  # 0-100
    interview_score = models.IntegerField(default=0)  # 0-100
    roadmap_progress = models.IntegerField(default=0)  # 0-100
    streak_days = models.IntegerField(default=0)  # Consecutive days of activity
    
    class Meta:
        ordering = ["-updated_at"]
    
    def __str__(self):
        return f"{self.user.email} - {self.overall_score}%"
