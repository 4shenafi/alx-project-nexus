"""
Payment models for NexusCommerce
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PaymentMethod(models.Model):
    """
    Payment method model
    """

    PAYMENT_TYPE_CHOICES = [
        ("credit_card", "Credit Card"),
        ("debit_card", "Debit Card"),
        ("paypal", "PayPal"),
        ("stripe", "Stripe"),
        ("bank_transfer", "Bank Transfer"),
        ("cash_on_delivery", "Cash on Delivery"),
        ("wallet", "Digital Wallet"),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPE_CHOICES, db_index=True
    )
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    processing_fee_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Processing fee as percentage",
    )
    processing_fee_fixed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Fixed processing fee",
    )
    min_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Minimum payment amount",
    )
    max_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Maximum payment amount",
    )
    configuration = models.JSONField(
        default=dict,
        blank=True,
        help_text="Payment method specific configuration",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_methods"
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["payment_type"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name


class Payment(models.Model):
    """
    Payment model
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
        ("partially_refunded", "Partially Refunded"),
    ]

    # Payment identification
    payment_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique payment identifier",
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payments",
        db_index=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", db_index=True
    )

    # Payment details
    payment_method = models.ForeignKey(
        PaymentMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Payment amount",
    )
    currency = models.CharField(
        max_length=3, default="USD", help_text="Payment currency code"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )

    # External payment provider information
    provider_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text="Payment ID from external provider",
    )
    provider_response = models.JSONField(
        default=dict, blank=True, help_text="Response from payment provider"
    )

    # Additional information
    processing_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Processing fee charged",
    )
    failure_reason = models.TextField(
        blank=True, null=True, help_text="Reason for payment failure"
    )
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "payments"
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["payment_id"]),
            models.Index(fields=["order"]),
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["provider_payment_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} - {self.order.order_number}"

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = self.generate_payment_id()
        super().save(*args, **kwargs)

    def generate_payment_id(self):
        """Generate a unique payment ID"""
        import uuid

        return f"PAY-{uuid.uuid4().hex[:8].upper()}"

    @property
    def is_successful(self):
        """Check if payment is successful"""
        return self.status == "completed"

    @property
    def is_failed(self):
        """Check if payment failed"""
        return self.status == "failed"


class Refund(models.Model):
    """
    Refund model
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    # Refund identification
    refund_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Unique refund identifier",
    )
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name="refunds",
        db_index=True,
    )
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="refunds",
        db_index=True,
    )

    # Refund details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Refund amount",
    )
    currency = models.CharField(
        max_length=3, default="USD", help_text="Refund currency code"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    reason = models.TextField(help_text="Reason for refund")

    # External provider information
    provider_refund_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        db_index=True,
        help_text="Refund ID from external provider",
    )
    provider_response = models.JSONField(
        default=dict, blank=True, help_text="Response from payment provider"
    )

    # Additional information
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_refunds",
        db_index=True,
    )
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "refunds"
        verbose_name = "Refund"
        verbose_name_plural = "Refunds"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["refund_id"]),
            models.Index(fields=["payment"]),
            models.Index(fields=["order"]),
            models.Index(fields=["status"]),
            models.Index(fields=["provider_refund_id"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Refund {self.refund_id} - {self.payment.payment_id}"

    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.refund_id = self.generate_refund_id()
        super().save(*args, **kwargs)

    def generate_refund_id(self):
        """Generate a unique refund ID"""
        import uuid

        return f"REF-{uuid.uuid4().hex[:8].upper()}"

    @property
    def is_successful(self):
        """Check if refund is successful"""
        return self.status == "completed"
