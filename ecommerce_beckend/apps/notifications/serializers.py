"""
Notification serializers for NexusCommerce
"""

from rest_framework import serializers

from .models import Notification, NotificationPreference, NotificationTemplate


class NotificationTemplateSerializer(serializers.ModelSerializer):
    """
    Notification template serializer
    """

    class Meta:
        model = NotificationTemplate
        fields = [
            "id",
            "name",
            "template_type",
            "subject",
            "body",
            "is_active",
            "variables",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class NotificationSerializer(serializers.ModelSerializer):
    """
    Notification serializer
    """

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    template_name = serializers.CharField(source="template.name", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "notification_id",
            "user",
            "user_name",
            "notification_type",
            "template",
            "template_name",
            "subject",
            "message",
            "delivery_method",
            "recipient_email",
            "recipient_phone",
            "status",
            "provider_message_id",
            "context_data",
            "failure_reason",
            "created_at",
            "updated_at",
            "sent_at",
            "delivered_at",
        ]
        read_only_fields = [
            "id",
            "notification_id",
            "user",
            "provider_message_id",
            "created_at",
            "updated_at",
            "sent_at",
            "delivered_at",
        ]


class NotificationCreateSerializer(serializers.ModelSerializer):
    """
    Notification creation serializer
    """

    class Meta:
        model = Notification
        fields = [
            "notification_type",
            "template",
            "subject",
            "message",
            "delivery_method",
            "recipient_email",
            "recipient_phone",
            "context_data",
        ]

    def validate_recipient_email(self, value):
        """Validate recipient email"""
        if not value and self.initial_data.get("delivery_method") == "email":
            raise serializers.ValidationError(
                "Email is required for email notifications."
            )
        return value

    def validate_recipient_phone(self, value):
        """Validate recipient phone"""
        if not value and self.initial_data.get("delivery_method") == "sms":
            raise serializers.ValidationError(
                "Phone number is required for SMS notifications."
            )
        return value


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    """
    Notification preference serializer
    """

    class Meta:
        model = NotificationPreference
        fields = [
            "id",
            "email_order_updates",
            "email_payment_updates",
            "email_promotions",
            "email_newsletter",
            "email_product_reviews",
            "sms_order_updates",
            "sms_payment_updates",
            "sms_promotions",
            "push_order_updates",
            "push_payment_updates",
            "push_promotions",
            "in_app_order_updates",
            "in_app_payment_updates",
            "in_app_promotions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
