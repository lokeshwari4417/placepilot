from rest_framework import serializers


class AIAssistRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=[
        "explain", "interview_questions", "resume_review", "project_suggestions", "plan",
    ])
    payload = serializers.DictField()
