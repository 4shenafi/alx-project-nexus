"""
Cart models for NexusCommerce
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Cart(models.Model):
    """
    Shopping cart model
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cart", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carts"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self):
        return f"Cart for {self.user.email}"

    @property
    def total_items(self):
        """Get total number of items in cart"""
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        """Calculate cart subtotal"""
        return sum(item.total_price for item in self.items.all())

    @property
    def is_empty(self):
        """Check if cart is empty"""
        return not self.items.exists()


class CartItem(models.Model):
    """
    Cart item model
    """

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", db_index=True
    )
    product_variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="cart_items",
        db_index=True,
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], help_text="Quantity in cart"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Price per unit when added to cart",
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Total price for this item",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "cart_items"
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = [["cart", "product_variant"]]
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["cart"]),
            models.Index(fields=["product_variant"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.cart.user.email} - {self.product_variant.product.name}"

    def save(self, *args, **kwargs):
        # Update unit price from current variant price
        self.unit_price = self.product_variant.price
        # Calculate total price
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        """Check if the product variant is available"""
        return self.product_variant.is_active and self.product_variant.is_in_stock

    @property
    def available_quantity(self):
        """Get available quantity for this variant"""
        return self.product_variant.stock_quantity

    def can_increase_quantity(self, additional_quantity=1):
        """Check if quantity can be increased"""
        return self.quantity + additional_quantity <= self.available_quantity
