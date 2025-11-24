import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Event
from .serializers import EventSerializer, EventInputSerializer, EventOutputSerializer

logger = logging.getLogger(__name__)

@extend_schema_view(
    list=extend_schema(
        summary="List user events",
        description="Retrieve all events assigned to the authenticated user",
        responses={200: EventOutputSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Get event details",
        description="Retrieve detailed information about a specific event",
        responses={200: EventOutputSerializer}
    ),
    create=extend_schema(
        summary="Create new event",
        description="Create a new event (personal or assigned to a collaborator)",
        request=EventInputSerializer,
        responses={201: EventOutputSerializer}
    ),
    update=extend_schema(
        summary="Update event",
        description="Update an existing event",
        request=EventInputSerializer,
        responses={200: EventOutputSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update event",
        description="Partially update an existing event",
        request=EventInputSerializer,
        responses={200: EventOutputSerializer}
    ),
    destroy=extend_schema(
        summary="Delete event",
        description="Delete an existing event",
        responses={204: None}
    )
)
class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EventInputSerializer
        return EventOutputSerializer

    def get_queryset(self):
        return Event.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        event = serializer.save(creator=self.request.user)
        logger.info(f"Event created: '{event.title}' by {self.request.user.username} for {event.assigned_to.username}")

    def perform_update(self, serializer):
        event = serializer.save()
        logger.info(f"Event updated: '{event.title}' by {self.request.user.username}")

    def perform_destroy(self, instance):
        logger.info(f"Event deleted: '{instance.title}' by {self.request.user.username}")
        instance.delete()
