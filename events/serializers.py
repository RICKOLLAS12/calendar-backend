from rest_framework import serializers
from .models import Event
from django.contrib.auth.models import User
from django.db import models
from collaborations.models import Collaboration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    assigned_to_user = UserSerializer(source='assigned_to', read_only=True)

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
        if user:
            # Filtrer les choix d'assignation aux collaborateurs
            collaborator_ids = Collaboration.objects.filter(
                user=user
            ).values_list('collaborator_id', flat=True)

            from django.contrib.auth.models import User
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