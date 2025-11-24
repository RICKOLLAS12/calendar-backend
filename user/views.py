from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer, UserCreateSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        summary="List all users",
        description="Retrieve a list of all users (admin only)",
        responses={200: UserSerializer(many=True)}
    ),
    retrieve=extend_schema(
        summary="Get user details",
        description="Retrieve detailed information about a specific user",
        responses={200: UserSerializer}
    ),
    create=extend_schema(
        summary="Create new user",
        description="Create a new user account (admin only)",
        request=UserCreateSerializer,
        responses={201: UserSerializer}
    ),
    update=extend_schema(
        summary="Update user",
        description="Update an existing user account",
        request=UserCreateSerializer,
        responses={200: UserSerializer}
    ),
    partial_update=extend_schema(
        summary="Partially update user",
        description="Partially update an existing user account",
        request=UserCreateSerializer,
        responses={200: UserSerializer}
    ),
    destroy=extend_schema(
        summary="Delete user",
        description="Delete an existing user account",
        responses={204: None}
    )
)
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
