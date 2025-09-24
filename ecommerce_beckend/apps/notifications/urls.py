"""
Notification URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "notifications"

# Create router for viewsets
router = DefaultRouter()
router.register(
    r"templates",
    views.NotificationTemplateViewSet,
    basename="notification-template",
)
router.register(r"", views.NotificationViewSet, basename="notification")
router.register(
    r"preferences",
    views.NotificationPreferenceViewSet,
    basename="notification-preference",
)

urlpatterns = [
    path("", include(router.urls)),
]
