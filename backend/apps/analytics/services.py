"""Business logic for the 'analytics' module, kept out of views."""

from .models import ReadinessScore


class ReadinessScoreService:
    """Service for calculating and managing readiness scores."""
    
    @staticmethod
    def get_or_create_score(user):
        """Get existing score or create default for user."""
        score, created = ReadinessScore.objects.get_or_create(
            user=user,
            defaults={
                "overall_score": 0,
                "coding_score": 0,
                "aptitude_score": 0,
                "resume_score": 0,
                "interview_score": 0,
                "roadmap_progress": 0,
                "streak_days": 0,
            }
        )
        return score
    
    @staticmethod
    def calculate_overall_score(score_obj):
        """Calculate overall score as weighted average of sub-scores."""
        # Weighted average: coding (30%), aptitude (20%), resume (25%), interview (25%)
        weighted = (
            score_obj.coding_score * 0.30 +
            score_obj.aptitude_score * 0.20 +
            score_obj.resume_score * 0.25 +
            score_obj.interview_score * 0.25
        )
        return int(weighted)
    
    @staticmethod
    def update_score(user, **sub_scores):
        """Update specific sub-scores and recalculate overall."""
        score = ReadinessScoreService.get_or_create_score(user)
        
        for field, value in sub_scores.items():
            if hasattr(score, field):
                setattr(score, field, min(100, max(0, value)))
        
        score.overall_score = ReadinessScoreService.calculate_overall_score(score)
        score.save()
        return score
