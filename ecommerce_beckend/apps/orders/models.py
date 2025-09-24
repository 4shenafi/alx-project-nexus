"""
Order models for NexusCommerce
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Order(models.Model):
    """
    Order model representing a customer's purchase
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("refunded", "Refunded"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("partially_refunded", "Partially Refunded"),
    ]

    # Order identification
    order_number = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique order number",
    )
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", db_index=True
    )

    # Order status
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        db_index=True,
    )

    # Pricing information
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Subtotal before taxes and shipping",
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Total tax amount",
    )
    shipping_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Shipping cost",
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Total discount amount",
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Final total amount",
    )

    # Address information
    shipping_address = models.JSONField(help_text="Shipping address at time of order")
    billing_address = models.JSONField(help_text="Billing address at time of order")

    # Additional information
    notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(
        blank=True, null=True, help_text="Internal notes for staff"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders"
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["customer"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    def generate_order_number(self):
        """Generate a unique order number"""
        import uuid

        return f"ORD-{uuid.uuid4().hex[:8].upper()}"

    @property
    def is_paid(self):
        """Check if order is paid"""
        return self.payment_status == "paid"

    @property
    def can_be_cancelled(self):
        """Check if order can be cancelled"""
        return self.status in ["pending", "confirmed", "processing"]


class OrderItem(models.Model):
    """
    Order item model - stores individual items in an order
    """

    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", db_index=True
    )

    # Product information (stored at time of purchase for historical integrity)
    product_variant_id = models.PositiveIntegerField(
        db_index=True,
        help_text="ID of the product variant at time of purchase",
    )
    product_name = models.CharField(
        max_length=255, help_text="Product name at time of purchase"
    )
    variant_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Variant name at time of purchase",
    )
    sku = models.CharField(max_length=100, help_text="SKU at time of purchase")

    # Pricing information (stored at time of purchase)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Unit price at time of purchase",
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Quantity ordered"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Total price for this item",
    )

    # Additional information
    product_attributes = models.JSONField(
        default=dict,
        blank=True,
        help_text="Product attributes at time of purchase",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_items"
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product_variant_id"]),
            models.Index(fields=["sku"]),
        ]

    def __str__(self):
        return f"{self.order.order_number} - {self.product_name}"

    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class OrderStatusHistory(models.Model):
    """
    Order status history model for tracking status changes
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="status_history",
        db_index=True,
    )
    status = models.CharField(
        max_length=20, choices=Order.STATUS_CHOICES, db_index=True
    )
    payment_status = models.CharField(
        max_length=20, choices=Order.PAYMENT_STATUS_CHOICES, db_index=True
    )
    notes = models.TextField(blank=True, null=True)
    changed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "order_status_history"
        verbose_name = "Order Status History"
        verbose_name_plural = "Order Status Histories"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order", "created_at"]),
            models.Index(fields=["status"]),
            models.Index(fields=["payment_status"]),
        ]

    def __str__(self):
        return f"{self.order.order_number} - {self.status} ({self.created_at})"


class ShippingMethod(models.Model):
    """
    Shipping method model
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    base_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Base shipping cost",
    )
    cost_per_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Additional cost per kg",
    )
    estimated_days_min = models.PositiveIntegerField(
        help_text="Minimum estimated delivery days"
    )
    estimated_days_max = models.PositiveIntegerField(
        help_text="Maximum estimated delivery days"
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_digital = models.BooleanField(
        default=False, help_text="Whether this method is for digital products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shipping_methods"
        verbose_name = "Shipping Method"
        verbose_name_plural = "Shipping Methods"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["is_active"]),
            models.Index(fields=["is_digital"]),
        ]

    def __str__(self):
        return self.name


class OrderShipping(models.Model):
    """
    Order shipping information model
    """

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="shipping", db_index=True
    )
    shipping_method = models.ForeignKey(
        ShippingMethod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    tracking_number = models.CharField(
        max_length=100, blank=True, null=True, db_index=True
    )
    carrier = models.CharField(
        max_length=100, blank=True, null=True, help_text="Shipping carrier"
    )
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    actual_delivery = models.DateTimeField(null=True, blank=True)
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Actual shipping cost",
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "order_shipping"
        verbose_name = "Order Shipping"
        verbose_name_plural = "Order Shipping"
        indexes = [
            models.Index(fields=["tracking_number"]),
            models.Index(fields=["carrier"]),
        ]

    def __str__(self):
        return f"{self.order.order_number} - Shipping"
