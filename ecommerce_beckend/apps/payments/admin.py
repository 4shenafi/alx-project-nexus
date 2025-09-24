"""
Admin configuration for payments app
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import Payment, PaymentMethod, Refund


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """
    PaymentMethod admin
    """

    list_display = [
        "name",
        "payment_type",
        "is_active",
        "processing_fee_percentage",
        "processing_fee_fixed",
        "min_amount",
        "max_amount",
        "created_at",
    ]
    list_filter = ["payment_type", "is_active", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["name"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Payment admin
    """

    list_display = [
        "payment_id",
        "order",
        "user",
        "payment_method",
        "amount",
        "currency",
        "status_display",
        "created_at",
    ]
    list_filter = ["status", "currency", "payment_method", "created_at"]
    search_fields = [
        "payment_id",
        "order__order_number",
        "user__email",
        "provider_payment_id",
    ]
    readonly_fields = [
        "payment_id",
        "provider_payment_id",
        "created_at",
        "updated_at",
        "processed_at",
        "completed_at",
    ]
    ordering = ["-created_at"]

    def status_display(self, obj):
        colors = {
            "pending": "orange",
            "processing": "blue",
            "completed": "green",
            "failed": "red",
            "cancelled": "gray",
            "refunded": "purple",
            "partially_refunded": "yellow",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    """
    Refund admin
    """

    list_display = [
        "refund_id",
        "payment",
        "order",
        "amount",
        "currency",
        "status_display",
        "processed_by",
        "created_at",
    ]
    list_filter = ["status", "currency", "created_at"]
    search_fields = [
        "refund_id",
        "payment__payment_id",
        "order__order_number",
        "provider_refund_id",
    ]
    readonly_fields = [
        "refund_id",
        "provider_refund_id",
        "created_at",
        "updated_at",
        "processed_at",
        "completed_at",
    ]
    ordering = ["-created_at"]

    def status_display(self, obj):
        colors = {
            "pending": "orange",
            "processing": "blue",
            "completed": "green",
            "failed": "red",
            "cancelled": "gray",
        }
        color = colors.get(obj.status, "black")
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display(),
        )

    status_display.short_description = "Status"
