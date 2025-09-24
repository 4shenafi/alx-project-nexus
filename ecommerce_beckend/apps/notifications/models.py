"""
Notification models for NexusCommerce
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class NotificationTemplate(models.Model):
    """
    Notification template model for reusable email/SMS templates
    """

    TEMPLATE_TYPE_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("push", "Push Notification"),
        ("in_app", "In-App Notification"),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    template_type = models.CharField(
        max_length=20, choices=TEMPLATE_TYPE_CHOICES, db_index=True
    )
    subject = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Email subject or notification title",
    )
    body = models.TextField(help_text="Template body with placeholders")
    is_active = models.BooleanField(default=True, db_index=True)
    variables = models.JSONField(
        default=list, blank=True, help_text="Available template variables"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification_templates"
        verbose_name = "Notification Template"
        verbose_name_plural = "Notification Templates"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["template_type"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"


class Notification(models.Model):
    """
    Notification model for tracking sent notifications
    """

    NOTIFICATION_TYPE_CHOICES = [
        ("order_confirmation", "Order Confirmation"),
        ("order_shipped", "Order Shipped"),
        ("order_delivered", "Order Delivered"),
        ("payment_confirmation", "Payment Confirmation"),
        ("payment_failed", "Payment Failed"),
        ("welcome", "Welcome"),
        ("email_verification", "Email Verification"),
        ("password_reset", "Password Reset"),
        ("low_stock", "Low Stock Alert"),
        ("vendor_approval", "Vendor Approval"),
        ("vendor_rejection", "Vendor Rejection"),
        ("product_review", "Product Review"),
        ("refund_processed", "Refund Processed"),
        ("newsletter", "Newsletter"),
        ("promotion", "Promotion"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("failed", "Failed"),
        ("bounced", "Bounced"),
    ]

    # Notification identification
    notification_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique notification identifier",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        db_index=True,
    )

    # Notification details
    notification_type = models.CharField(
        max_length=30, choices=NOTIFICATION_TYPE_CHOICES, db_index=True
    )
    template = models.ForeignKey(
        NotificationTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(help_text="Notification message content")

    # Delivery information
    delivery_method = models.CharField(
        max_length=20,
        choices=NotificationTemplate.TEMPLATE_TYPE_CHOICES,
        db_index=True,
    )
    recipient_email = models.EmailField(blank=True, null=True, db_index=True)
    recipient_phone = models.CharField(
        max_length=20, blank=True, null=True, db_index=True
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )

    # External provider information
    provider_message_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text="Message ID from external provider",
    )
    provider_response = models.JSONField(
        default=dict,
        blank=True,
        help_text="Response from notification provider",
    )

    # Additional information
    context_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Context data used for template rendering",
    )
    failure_reason = models.TextField(
        blank=True, null=True, help_text="Reason for notification failure"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications"
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["notification_id"]),
            models.Index(fields=["user"]),
            models.Index(fields=["notification_type"]),
            models.Index(fields=["delivery_method"]),
            models.Index(fields=["status"]),
            models.Index(fields=["recipient_email"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.notification_type} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.notification_id:
            self.notification_id = self.generate_notification_id()
        super().save(*args, **kwargs)

    def generate_notification_id(self):
        """Generate a unique notification ID"""
        import uuid

        return f"NOTIF-{uuid.uuid4().hex[:8].upper()}"

    @property
    def is_successful(self):
        """Check if notification was successful"""
        return self.status in ["sent", "delivered"]


class NotificationPreference(models.Model):
    """
    User notification preferences model
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="notification_preferences",
        db_index=True,
    )

    # Email preferences
    email_order_updates = models.BooleanField(default=True)
    email_payment_updates = models.BooleanField(default=True)
    email_promotions = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=True)
    email_product_reviews = models.BooleanField(default=True)

    # SMS preferences
    sms_order_updates = models.BooleanField(default=False)
    sms_payment_updates = models.BooleanField(default=False)
    sms_promotions = models.BooleanField(default=False)

    # Push notification preferences
    push_order_updates = models.BooleanField(default=True)
    push_payment_updates = models.BooleanField(default=True)
    push_promotions = models.BooleanField(default=True)

    # In-app notification preferences
    in_app_order_updates = models.BooleanField(default=True)
    in_app_payment_updates = models.BooleanField(default=True)
    in_app_promotions = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification_preferences"
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"

    def __str__(self):
        return f"Notification Preferences - {self.user.email}"
