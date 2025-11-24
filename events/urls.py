from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')

app_name = 'events'

urlpatterns = [
    path('', include(router.urls)),
    # Override the detail route to specify int type for better Swagger docs
    path('events/<int:pk>/', EventViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='event-detail'),
]