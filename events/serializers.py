from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User
from django.db import models
from collaborations.models import Collaboration
from drf_spectacular.utils import extend_schema_field, OpenApiExample

class EventUserSerializer(serializers.ModelSerializer):
    """Serializer for User information in events"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventInputSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating events"""

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'start_date', 'end_date',
            'location', 'color', 'assigned_to'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            # Filtrer les choix d'assignation aux collaborateurs
            collaborator_ids = Collaboration.objects.filter(
                user=user
            ).values_list('collaborator_id', flat=True)

            choices = User.objects.filter(
                models.Q(id=user.id) | models.Q(id__in=collaborator_ids)
            )

            self.fields['assigned_to'] = serializers.PrimaryKeyRelatedField(
                queryset=choices,
                help_text="ID of the user to assign this event to (yourself or collaborators)"
            )

class EventOutputSerializer(serializers.ModelSerializer):
    """Serializer for reading events"""
    creator = EventUserSerializer(read_only=True)
    assigned_to_user = EventUserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type',
            'start_date', 'end_date', 'location', 'color',
            'is_completed', 'creator', 'assigned_to', 'assigned_to_user',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'creator', 'event_type', 'created_at', 'updated_at']

class EventSerializer(serializers.ModelSerializer):
    """Combined serializer for backward compatibility"""
    creator = EventUserSerializer(read_only=True)
    assigned_to_user = EventUserSerializer(source='assigned_to', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type',
            'start_date', 'end_date', 'location', 'color',
            'is_completed', 'creator', 'assigned_to', 'assigned_to_user',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['creator', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            # Filtrer les choix d'assignation aux collaborateurs
            collaborator_ids = Collaboration.objects.filter(
                user=user
            ).values_list('collaborator_id', flat=True)

            choices = User.objects.filter(
                models.Q(id=user.id) | models.Q(id__in=collaborator_ids)
            )

            self.fields['assigned_to'].queryset = choices

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user

        # Définir le type d'event
        if validated_data['assigned_to'] == self.context['request'].user:
            validated_data['event_type'] = 'personal'
        else:
            validated_data['event_type'] = 'task'

        return super().create(validated_data)