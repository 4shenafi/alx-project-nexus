"""
Notification views for NexusCommerce
"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdminUser, IsOwnerOrAdmin

from .models import Notification, NotificationPreference, NotificationTemplate
from .serializers import (NotificationCreateSerializer,
                          NotificationPreferenceSerializer,
                          NotificationSerializer,
                          NotificationTemplateSerializer)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """
    Notification template viewset
    """

    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="List notification templates",
        description="Get all notification templates (admin only)",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create notification template",
        description="Create a new notification template (admin only)",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = serializer.save()

        return Response(
            {
                "status": "success",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class NotificationViewSet(viewsets.ModelViewSet):
    """
    Notification viewset
    """

    queryset = Notification.objects.select_related("user", "template")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return NotificationCreateSerializer
        return NotificationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action in ["create"]:
            self.permission_classes = [IsAdminUser]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by user role
        if self.request.user.is_admin:
            return queryset
        else:
            # Users can only see their own notifications
            return queryset.filter(user=self.request.user)

    @extend_schema(
        summary="List notifications",
        description="Get all notifications for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get notification details",
        description="Get detailed information about a specific notification",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create notification",
        description="Create a new notification (admin only)",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()

        # Send notification (simplified - in real implementation, use Celery task)
        notification = self.send_notification(notification)

        return Response(
            {
                "status": "success",
                "data": NotificationSerializer(notification).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def send_notification(self, notification):
        """Send notification (simplified implementation)"""
        # In a real implementation, this would integrate with email/SMS providers

        try:
            # Simulate sending notification
            notification.status = "sent"
            notification.sent_at = timezone.now()
            notification.provider_message_id = f"MSG_{notification.notification_id}"
            notification.save()

            # Simulate delivery
            notification.status = "delivered"
            notification.delivered_at = timezone.now()
            notification.save()

        except Exception as e:
            # Handle notification failure
            notification.status = "failed"
            notification.failure_reason = str(e)
            notification.save()

        return notification

    @extend_schema(
        summary="Get my notifications",
        description="Get all notifications for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def my_notifications(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Mark notification as read",
        description="Mark a notification as read",
        responses={200: {"description": "Notification marked as read"}},
    )
    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        # In a real implementation, you might have an 'is_read' field
        # For now, we'll just return success
        return Response(
            {
                "status": "success",
                "data": {"message": "Notification marked as read"},
            },
            status=status.HTTP_200_OK,
        )


class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    """
    Notification preference viewset
    """

    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def get_object(self):
        """Get or create notification preferences for the current user"""
        preferences, created = NotificationPreference.objects.get_or_create(
            user=self.request.user
        )
        return preferences

    @extend_schema(
        summary="Get notification preferences",
        description="Get notification preferences for the current user",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        preferences = self.get_object()
        serializer = self.get_serializer(preferences)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Update notification preferences",
        description="Update notification preferences for the current user",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def partial_update(self, request, *args, **kwargs):
        preferences = self.get_object()
        serializer = self.get_serializer(preferences, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        preferences = serializer.save()

        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )
