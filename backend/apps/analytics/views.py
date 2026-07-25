from rest_framework import generics, permissions

from .models import ReadinessScore
from .serializers import ReadinessScoreSerializer
from .services import ReadinessScoreService


class ReadinessScoreView(generics.RetrieveAPIView):
    """Get the current user's readiness score."""
    
    serializer_class = ReadinessScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return ReadinessScoreService.get_or_create_score(self.request.user)
