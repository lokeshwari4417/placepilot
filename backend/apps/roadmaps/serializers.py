from rest_framework import serializers

from .models import Roadmap, RoadmapProgress, RoadmapTopic


class RoadmapTopicSerializer(serializers.ModelSerializer):
    """Serializer for RoadmapTopic model."""
    
    class Meta:
        model = RoadmapTopic
        fields = ["id", "title", "description", "order", "resources"]
        read_only_fields = ["id"]


class RoadmapSerializer(serializers.ModelSerializer):
    """Serializer for Roadmap model with topics."""
    
    topics = RoadmapTopicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Roadmap
        fields = [
            "id",
            "title",
            "description",
            "target_role",
            "estimated_weeks",
            "topics",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class RoadmapProgressSerializer(serializers.ModelSerializer):
    """Serializer for RoadmapProgress model."""
    
    roadmap = RoadmapSerializer(read_only=True)
    completed_topics = RoadmapTopicSerializer(many=True, read_only=True)
    completion_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = RoadmapProgress
        fields = [
            "id",
            "roadmap",
            "status",
            "completed_topics",
            "completion_percentage",
            "started_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class TopicActionSerializer(serializers.Serializer):
    """Serializer for topic completion/uncompletion actions."""
    
    topic_id = serializers.UUIDField()
