"""
Admin configuration for carts app
"""

from django.contrib import admin

from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Cart admin
    """

    list_display = [
        "user",
        "total_items",
        "subtotal",
        "is_empty",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__email", "user__first_name", "user__last_name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-updated_at"]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    CartItem admin
    """

    list_display = [
        "cart",
        "product_variant",
        "quantity",
        "unit_price",
        "total_price",
        "is_available",
        "created_at",
        "updated_at",
    ]
    list_filter = ["created_at", "updated_at"]
    search_fields = [
        "cart__user__email",
        "product_variant__product__name",
        "product_variant__sku",
    ]
    readonly_fields = ["unit_price", "total_price", "created_at", "updated_at"]
    ordering = ["-created_at"]
