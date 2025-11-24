from django.db import models
from django.contrib.auth.models import User

class CollaborationRequest(models.Model):
    """Demande de collaboration envoyée d'un user à un autre"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['sender', 'receiver']  # Évite les doublons
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username} ({self.status})"

    def accept(self):
        """Accepte la demande et crée une collaboration"""
        self.status = 'accepted'
        self.save()
        # Créer la collaboration bidirectionnelle
        Collaboration.objects.get_or_create(user=self.sender, collaborator=self.receiver)
        Collaboration.objects.get_or_create(user=self.receiver, collaborator=self.sender)

    def reject(self):
        self.status = 'rejected'
        self.save()


class Collaboration(models.Model):
    """Relation de collaboration entre deux users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations')
    collaborator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborated_with')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'collaborator']
        ordering = ['collaborator__username']

    def __str__(self):
        return f"{self.user.username} <-> {self.collaborator.username}"
