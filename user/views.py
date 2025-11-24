from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs (réservé aux admins)
    """
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activer un utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'message': f'Utilisateur {user.username} activé'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Désactiver un utilisateur"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'message': f'Utilisateur {user.username} désactivé'})

    @action(detail=True, methods=['post'])
    def make_staff(self, request, pk=None):
        """Donner les droits staff"""
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'message': f'{user.username} est maintenant staff'})

    @action(detail=True, methods=['post'])
    def remove_staff(self, request, pk=None):
        """Retirer les droits staff"""
        user = self.get_object()
        user.is_staff = False
        user.save()
        return Response({'message': f'{user.username} n\'est plus staff'})
