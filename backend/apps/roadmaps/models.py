from django.db import models

from apps.core.models import BaseModel


class Roadmap(BaseModel):
    """Learning roadmap for a specific target role."""
    
    class TargetRole(models.TextChoices):
        FRONTEND = "frontend", "Frontend Developer"
        BACKEND = "backend", "Backend Developer"
        FULL_STACK = "full_stack", "Full Stack Developer"
        DATA_ANALYST = "data_analyst", "Data Analyst"
        DATA_SCIENTIST = "data_scientist", "Data Scientist"
        AI_ML = "ai_ml", "AI/ML Engineer"
        DEVOPS = "devops", "DevOps Engineer"
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_role = models.CharField(max_length=50, choices=TargetRole.choices, unique=True)
    estimated_weeks = models.IntegerField(default=12)
    
    class Meta:
        ordering = ["target_role"]
    
    def __str__(self):
        return self.title


class RoadmapTopic(BaseModel):
    """Individual topic within a roadmap."""
    
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name="topics")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    resources = models.JSONField(default=dict, blank=True)  # Links, videos, docs
    
    class Meta:
        ordering = ["roadmap", "order"]
        unique_together = [["roadmap", "order"]]
    
    def __str__(self):
        return f"{self.roadmap.title} - {self.title}"


class RoadmapProgress(BaseModel):
    """User's progress through a roadmap."""
    
    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
    
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="roadmap_progress")
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name="user_progress")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    completed_topics = models.ManyToManyField(RoadmapTopic, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["-updated_at"]
        unique_together = [["user", "roadmap"]]
    
    def __str__(self):
        return f"{self.user.email} - {self.roadmap.title}"
    
    @property
    def completion_percentage(self):
        """Calculate completion percentage based on topics."""
        total_topics = self.roadmap.topics.count()
        if total_topics == 0:
            return 0
        completed_count = self.completed_topics.count()
        return int((completed_count / total_topics) * 100)
