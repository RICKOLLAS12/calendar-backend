from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Q
from .models import CollaborationRequest, Collaboration
from .serializers import CollaborationRequestSerializer, CollaborationSerializer, SendCollaborationRequestSerializer

class SendCollaborationRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SendCollaborationRequestSerializer

    def post(self, request):
        serializer = SendCollaborationRequestSerializer(data=request.data)
        if serializer.is_valid():
            receiver_username = serializer.validated_data['receiver_username']
            try:
                receiver = User.objects.get(username=receiver_username)

                if receiver == request.user:
                    return Response({'error': 'Vous ne pouvez pas vous ajouter vous-même.'}, status=status.HTTP_400_BAD_REQUEST)

                # Vérifier si déjà collaborateurs
                if Collaboration.objects.filter(user=request.user, collaborator=receiver).exists():
                    return Response({'message': 'Vous êtes déjà collaborateurs.'}, status=status.HTTP_200_OK)

                # Vérifier si demande existe déjà
                existing = CollaborationRequest.objects.filter(
                    sender=request.user,
                    receiver=receiver,
                    status='pending'
                ).exists()

                if existing:
                    return Response({'message': 'Vous avez déjà envoyé une demande à cet utilisateur.'}, status=status.HTTP_200_OK)
                else:
                    CollaborationRequest.objects.create(
                        sender=request.user,
                        receiver=receiver,
                        message=serializer.validated_data.get('message', '')
                    )
                    return Response({'message': f'Demande envoyée à {receiver.username}.'}, status=status.HTTP_201_CREATED)

            except User.DoesNotExist:
                return Response({'error': 'Utilisateur introuvable.'}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollaborationRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollaborationRequestSerializer

    def get(self, request):
        received_requests = CollaborationRequest.objects.filter(
            receiver=request.user,
            status='pending'
        )
        sent_requests = CollaborationRequest.objects.filter(
            sender=request.user
        )

        return Response({
            'received': CollaborationRequestSerializer(received_requests, many=True).data,
            'sent': CollaborationRequestSerializer(sent_requests, many=True).data
        })

class AcceptCollaborationRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None  # No input serializer needed for POST with no body

    def post(self, request, pk):
        try:
            collab_request = CollaborationRequest.objects.get(
                pk=pk,
                receiver=request.user,
                status='pending'
            )
            collab_request.accept()
            return Response({'message': f'Vous êtes maintenant collaborateur avec {collab_request.sender.username}.'})
        except CollaborationRequest.DoesNotExist:
            return Response({'error': 'Demande introuvable.'}, status=status.HTTP_404_NOT_FOUND)

class RejectCollaborationRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, pk):
        try:
            collab_request = CollaborationRequest.objects.get(
                pk=pk,
                receiver=request.user,
                status='pending'
            )
            collab_request.reject()
            return Response({'message': 'Demande refusée.'})
        except CollaborationRequest.DoesNotExist:
            return Response({'error': 'Demande introuvable.'}, status=status.HTTP_404_NOT_FOUND)

class CollaboratorListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CollaborationSerializer

    def get(self, request):
        collaborations = Collaboration.objects.filter(user=request.user)
        return Response(CollaborationSerializer(collaborations, many=True).data)

class RemoveCollaboratorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, pk):
        try:
            collaboration = Collaboration.objects.get(pk=pk, user=request.user)
            collaborator = collaboration.collaborator

            # Supprimer les deux côtés de la collaboration
            Collaboration.objects.filter(
                Q(user=request.user, collaborator=collaborator) |
                Q(user=collaborator, collaborator=request.user)
            ).delete()

            return Response({'message': f'Collaboration avec {collaborator.username} supprimée.'})
        except Collaboration.DoesNotExist:
            return Response({'error': 'Collaboration introuvable.'}, status=status.HTTP_404_NOT_FOUND)
