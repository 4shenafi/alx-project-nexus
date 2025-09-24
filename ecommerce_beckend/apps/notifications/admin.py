"""
Admin configuration for notifications app
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Notification, NotificationPreference, NotificationTemplate


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    """
    NotificationTemplate admin
    """

    list_display = [
        "name",
        "template_type",
        "is_active",
        "created_at",
        "updated_at",
    ]
    list_filter = ["template_type", "is_active", "created_at"]
    search_fields = ["name", "subject", "body"]
    ordering = ["name"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Notification admin
    """

    list_display = [
        "notification_id",
        "user",
        "notification_type",
        "delivery_method",
        "status_display",
        "recipient_email",
        "created_at",
    ]
    list_filter = [
        "notification_type",
        "delivery_method",
        "status",
        "created_at",
    ]
    search_fields = [
        "notification_id",
        "user__email",
        "recipient_email",
        "provider_message_id",
    ]
    readonly_fields = [
        "notification_id",
        "provider_message_id",
        "created_at",
        "updated_at",
        "sent_at",
        "delivered_at",
    ]
    ordering = ["-created_at"]

    def status_display(self, obj):
        colors = {
            "pending": "orange",
            "sent": "blue",
            "delivered": "green",
            "failed": "red",
            "bounced": "purple",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    """
    NotificationPreference admin
    """

    list_display = [
        "user",
        "email_order_updates",
        "email_promotions",
        "sms_order_updates",
        "push_order_updates",
        "created_at",
    ]
    list_filter = [
        "email_order_updates",
        "email_promotions",
        "sms_order_updates",
        "push_order_updates",
        "created_at",
    ]
    search_fields = ["user__email"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
