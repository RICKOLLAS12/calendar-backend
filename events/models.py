from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('personal', 'Personnel'),
        ('task', 'Tâche assignée'),
    ]

    # Créateur de l'event
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

    # Personne à qui l'event est assigné (peut être le créateur ou un collaborateur)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_events')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPE_CHOICES, default='personal')

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True)

    # Statut pour les tâches
    is_completed = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#3788d8')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        if self.creator != self.assigned_to:
            return f"{self.title} (de {self.creator.username} pour {self.assigned_to.username})"
        return f"{self.title} - {self.assigned_to.username}"

    def is_task(self):
        return self.creator != self.assigned_to
