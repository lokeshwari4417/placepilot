from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AIAssistRequestSerializer
from .services import AIAssistantService


class AIAssistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AIAssistRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = AIAssistantService()
        try:
            result = service.handle(
                serializer.validated_data["type"],
                serializer.validated_data["payload"],
            )
        except NotImplementedError:
            return Response(
                {"detail": "AI provider not yet configured."},
                status=status.HTTP_501_NOT_IMPLEMENTED,
            )
        return Response({"result": result})
