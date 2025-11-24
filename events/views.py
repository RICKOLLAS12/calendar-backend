import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

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
