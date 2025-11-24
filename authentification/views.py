import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, update_session_auth_hash
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from calendar_management.throttling import LoginThrottle, RegisterThrottle

# Get logger for this module
logger = logging.getLogger(__name__)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=8, write_only=True)

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError(_("Les nouveaux mots de passe ne correspondent pas."))
        return data

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    throttle_classes = [LoginThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                logger.info(f"User {username} logged in successfully")
                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            else:
                logger.warning(f"Failed login attempt for username: {username}")
                return Response({'error': _('Identifiants invalides')}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({'error': _('Nom d\'utilisateur déjà pris')}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'error': _('Email déjà utilisé')}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                refresh = RefreshToken.for_user(user)

                logger.info(f"New user registered: {username} (ID: {user.id})")

                return Response({
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Registration failed for {username}: {str(e)}")
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            # Vérifier l'ancien mot de passe
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'error': _('Ancien mot de passe incorrect')}, status=status.HTTP_400_BAD_REQUEST)

            # Changer le mot de passe
            user.set_password(serializer.validated_data['new_password'])
            user.save()

            # Réinitialiser le flag must_change_password
            if hasattr(user, 'profile'):
                user.profile.must_change_password = False
                user.profile.save()

            # Mettre à jour la session pour éviter la déconnexion
            update_session_auth_hash(request, user)

            return Response({'message': _('Mot de passe changé avec succès')})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
