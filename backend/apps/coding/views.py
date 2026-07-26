from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Problem, Submission
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    ProblemSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
)
from .services import CodeExecutionService


class ProblemViewSet(ModelViewSet):
    """ViewSet for listing and retrieving coding problems."""
    
    queryset = Problem.objects.prefetch_related("test_cases")
    serializer_class = ProblemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        """Only admins can create/update/delete problems."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        """Filter out hidden test cases for non-admin users."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.prefetch_related(
                "test_cases"
            )  # Will need custom filtering in serializer
        return queryset


class SubmissionListView(generics.ListCreateAPIView):
    """List user's submissions or create a new one."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return SubmissionCreateSerializer
        return SubmissionSerializer
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).select_related("problem")
    
    def post(self, request, *args, **kwargs):
        """Create and execute a code submission."""
        problem_id = kwargs.get("problem_id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            problem = Problem.objects.get(id=problem_id)
            submission = CodeExecutionService.create_submission(
                request.user,
                problem,
                serializer.validated_data["code"],
                serializer.validated_data["language"]
            )
            
            # Update analytics coding score on acceptance
            if submission.status == Submission.Status.ACCEPTED:
                from apps.analytics.services import ReadinessScoreService
                current_score = ReadinessScoreService.get_or_create_score(request.user)
                new_score = min(100, current_score.coding_score + 5)
                ReadinessScoreService.update_score(request.user, coding_score=new_score)
            
            return Response(
                SubmissionSerializer(submission).data,
                status=status.HTTP_201_CREATED
            )
        except Problem.DoesNotExist:
            return Response(
                {"detail": "Problem not found."},
                status=status.HTTP_404_NOT_FOUND
            )


class SubmissionDetailView(generics.RetrieveAPIView):
    """Retrieve a specific submission."""
    
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).select_related("problem")
