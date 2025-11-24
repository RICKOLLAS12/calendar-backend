from rest_framework import serializers
from .models import CollaborationRequest, Collaboration
from django.contrib.auth.models import User

class CollaborationRequestSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(read_only=True)
    receiver = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = CollaborationRequest
        fields = ['id', 'sender', 'receiver', 'status', 'message', 'created_at', 'updated_at']
        read_only_fields = ['sender', 'created_at', 'updated_at']

class CollaborationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    collaborator = serializers.StringRelatedField()

    class Meta:
        model = Collaboration
        fields = ['id', 'user', 'collaborator', 'created_at']
        read_only_fields = ['created_at']

class SendCollaborationRequestSerializer(serializers.Serializer):
    receiver_username = serializers.CharField(max_length=150)
    message = serializers.CharField(required=False, allow_blank=True)