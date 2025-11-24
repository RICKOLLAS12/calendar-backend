from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(assigned_to=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
