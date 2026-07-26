from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Roadmap, RoadmapProgress, RoadmapTopic
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    RoadmapProgressSerializer,
    RoadmapSerializer,
    TopicActionSerializer,
)
from .services import RoadmapService


class RoadmapViewSet(ModelViewSet):
    """ViewSet for listing and retrieving roadmaps (read-only for students)."""
    
    queryset = Roadmap.objects.prefetch_related("topics")
    serializer_class = RoadmapSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Only admins can create/update/delete roadmaps."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class RoadmapProgressListView(generics.ListCreateAPIView):
    """List user's roadmap progress or start a new roadmap."""
    
    serializer_class = RoadmapProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return RoadmapProgress.objects.filter(user=self.request.user).select_related("roadmap")
    
    def post(self, request):
        """Start a roadmap."""
        roadmap_id = request.data.get("roadmap_id")
        try:
            roadmap = Roadmap.objects.get(id=roadmap_id)
            progress = RoadmapService.start_roadmap(request.user, roadmap)
            serializer = self.get_serializer(progress)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Roadmap.DoesNotExist:
            return Response(
                {"detail": "Roadmap not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class RoadmapProgressDetailView(generics.RetrieveUpdateAPIView):
    """Retrieve or update specific roadmap progress."""
    
    serializer_class = RoadmapProgressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return RoadmapProgress.objects.filter(user=self.request.user).select_related("roadmap")
    
    def get_object(self):
        """Get progress by roadmap ID instead of progress ID."""
        roadmap_id = self.kwargs.get("roadmap_id")
        return RoadmapService.get_or_create_progress(self.request.user, roadmap_id)


class CompleteTopicView(generics.GenericAPIView):
    """Mark a topic as completed."""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TopicActionSerializer
    
    def post(self, request, roadmap_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            roadmap = Roadmap.objects.get(id=roadmap_id)
            topic = RoadmapTopic.objects.get(id=serializer.validated_data["topic_id"], roadmap=roadmap)
            progress = RoadmapService.complete_topic(request.user, roadmap, topic)
            
            # Update analytics roadmap progress
            from apps.analytics.services import ReadinessScoreService
            ReadinessScoreService.update_score(
                request.user,
                roadmap_progress=progress.completion_percentage
            )
            
            return Response(
                RoadmapProgressSerializer(progress).data,
                status=status.HTTP_200_OK
            )
        except (Roadmap.DoesNotExist, RoadmapTopic.DoesNotExist):
            return Response(
                {"detail": "Roadmap or topic not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class UncompleteTopicView(generics.GenericAPIView):
    """Remove a topic from completed list."""
    
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TopicActionSerializer
    
    def post(self, request, roadmap_id):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            roadmap = Roadmap.objects.get(id=roadmap_id)
            topic = RoadmapTopic.objects.get(id=serializer.validated_data["topic_id"], roadmap=roadmap)
            progress = RoadmapService.uncomplete_topic(request.user, roadmap, topic)
            
            # Update analytics roadmap progress
            from apps.analytics.services import ReadinessScoreService
            ReadinessScoreService.update_score(
                request.user,
                roadmap_progress=progress.completion_percentage
            )
            
            return Response(
                RoadmapProgressSerializer(progress).data,
                status=status.HTTP_200_OK
            )
        except (Roadmap.DoesNotExist, RoadmapTopic.DoesNotExist):
            return Response(
                {"detail": "Roadmap or topic not found."},
                status=status.HTTP_404_NOT_FOUND
            )
