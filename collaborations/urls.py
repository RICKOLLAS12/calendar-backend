from django.urls import path
from .views import (
    SendCollaborationRequestAPIView,
    CollaborationRequestListAPIView,
    AcceptCollaborationRequestAPIView,
    RejectCollaborationRequestAPIView,
    CollaboratorListAPIView,
    RemoveCollaboratorAPIView,
)

app_name = 'collaborations'

urlpatterns = [
    path('send/', SendCollaborationRequestAPIView.as_view(), name='send_request'),
    path('requests/', CollaborationRequestListAPIView.as_view(), name='request_list'),
    path('requests/<int:pk>/accept/', AcceptCollaborationRequestAPIView.as_view(), name='accept_request'),
    path('requests/<int:pk>/reject/', RejectCollaborationRequestAPIView.as_view(), name='reject_request'),
    path('collaborators/', CollaboratorListAPIView.as_view(), name='collaborator_list'),
    path('collaborators/<int:pk>/remove/', RemoveCollaboratorAPIView.as_view(), name='remove_collaborator'),
]