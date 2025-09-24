"""
Admin configuration for orders app
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (Order, OrderItem, OrderShipping, OrderStatusHistory,
                     ShippingMethod)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Order admin
    """

    list_display = [
        "order_number",
        "customer",
        "status_display",
        "payment_status_display",
        "total_amount",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "created_at"]
    search_fields = [
        "order_number",
        "customer__email",
        "customer__first_name",
        "customer__last_name",
    ]
    readonly_fields = ["order_number", "created_at", "updated_at"]
    ordering = ["-created_at"]

    def status_display(self, obj):
        colors = {
            "pending": "orange",
            "confirmed": "blue",
            "processing": "purple",
            "shipped": "teal",
            "delivered": "green",
            "cancelled": "red",
            "refunded": "gray",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"

    def payment_status_display(self, obj):
        colors = {
            "pending": "orange",
            "paid": "green",
            "failed": "red",
            "refunded": "gray",
            "partially_refunded": "yellow",
        }
        color = colors.get(obj.payment_status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display(),
        )

    payment_status_display.short_description = "Payment Status"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    OrderItem admin
    """

    list_display = [
        "order",
        "product_name",
        "variant_name",
        "sku",
        "quantity",
        "unit_price",
        "total_price",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["order__order_number", "product_name", "sku"]
    ordering = ["-created_at"]


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    """
    OrderStatusHistory admin
    """

    list_display = [
        "order",
        "status",
        "payment_status",
        "changed_by",
        "created_at",
    ]
    list_filter = ["status", "payment_status", "created_at"]
    search_fields = ["order__order_number", "changed_by__email"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    """
    ShippingMethod admin
    """

    list_display = [
        "name",
        "base_cost",
        "cost_per_kg",
        "estimated_days_min",
        "estimated_days_max",
        "is_active",
        "is_digital",
        "created_at",
    ]
    list_filter = ["is_active", "is_digital", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["name"]


@admin.register(OrderShipping)
class OrderShippingAdmin(admin.ModelAdmin):
    """
    OrderShipping admin
    """

    list_display = [
        "order",
        "shipping_method",
        "tracking_number",
        "carrier",
        "shipping_cost",
        "estimated_delivery",
        "actual_delivery",
        "created_at",
    ]
    list_filter = ["carrier", "created_at"]
    search_fields = ["order__order_number", "tracking_number", "carrier"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
