"""Business logic for the 'roadmaps' module, kept out of views."""

from django.utils import timezone

from .models import Roadmap, RoadmapProgress, RoadmapTopic


class RoadmapService:
    """Service for roadmap-related business logic."""
    
    @staticmethod
    def get_or_create_progress(user, roadmap):
        """Get existing progress or create new for user-roadmap pair."""
        progress, created = RoadmapProgress.objects.get_or_create(
            user=user,
            roadmap=roadmap,
            defaults={"status": RoadmapProgress.Status.NOT_STARTED}
        )
        return progress
    
    @staticmethod
    def start_roadmap(user, roadmap):
        """Mark a roadmap as in progress."""
        progress = RoadmapService.get_or_create_progress(user, roadmap)
        if progress.status == RoadmapProgress.Status.NOT_STARTED:
            progress.status = RoadmapProgress.Status.IN_PROGRESS
            progress.started_at = timezone.now()
            progress.save()
        return progress
    
    @staticmethod
    def complete_topic(user, roadmap, topic):
        """Mark a topic as completed for a user's roadmap progress."""
        progress = RoadmapService.get_or_create_progress(user, roadmap)
        progress.completed_topics.add(topic)
        
        # Update status if all topics completed
        total_topics = roadmap.topics.count()
        if progress.completed_topics.count() == total_topics and total_topics > 0:
            progress.status = RoadmapProgress.Status.COMPLETED
            progress.completed_at = timezone.now()
        
        progress.save()
        return progress
    
    @staticmethod
    def uncomplete_topic(user, roadmap, topic):
        """Remove a topic from completed list."""
        progress = RoadmapService.get_or_create_progress(user, roadmap)
        progress.completed_topics.remove(topic)
        
        # Update status if was completed but now isn't
        if progress.status == RoadmapProgress.Status.COMPLETED:
            progress.status = RoadmapProgress.Status.IN_PROGRESS
            progress.completed_at = None
        
        progress.save()
        return progress
