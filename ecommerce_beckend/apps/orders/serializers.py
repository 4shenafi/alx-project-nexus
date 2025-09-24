"""
Order serializers for NexusCommerce
"""

from decimal import Decimal

from rest_framework import serializers

from apps.carts.models import CartItem
from apps.products.models import ProductVariant

from .models import (Order, OrderItem, OrderShipping, OrderStatusHistory,
                     ShippingMethod)


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Order item serializer
    """

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product_variant_id",
            "product_name",
            "variant_name",
            "sku",
            "unit_price",
            "quantity",
            "total_price",
            "product_attributes",
        ]
        read_only_fields = ["id"]


class OrderShippingSerializer(serializers.ModelSerializer):
    """
    Order shipping serializer
    """

    shipping_method_name = serializers.CharField(
        source="shipping_method.name", read_only=True
    )

    class Meta:
        model = OrderShipping
        fields = [
            "id",
            "shipping_method",
            "shipping_method_name",
            "tracking_number",
            "carrier",
            "estimated_delivery",
            "actual_delivery",
            "shipping_cost",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Order serializer
    """

    items = OrderItemSerializer(many=True, read_only=True)
    shipping = OrderShippingSerializer(read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    customer_email = serializers.CharField(source="customer.email", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer",
            "customer_name",
            "customer_email",
            "status",
            "payment_status",
            "subtotal",
            "tax_amount",
            "shipping_amount",
            "discount_amount",
            "total_amount",
            "shipping_address",
            "billing_address",
            "notes",
            "internal_notes",
            "items",
            "shipping",
            "created_at",
            "updated_at",
            "confirmed_at",
            "shipped_at",
            "delivered_at",
        ]
        read_only_fields = [
            "id",
            "order_number",
            "customer",
            "created_at",
            "updated_at",
            "confirmed_at",
            "shipped_at",
            "delivered_at",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    """
    Order list serializer for listing views
    """

    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "customer_name",
            "item_count",
            "status",
            "payment_status",
            "total_amount",
            "created_at",
            "updated_at",
        ]

    def get_item_count(self, obj):
        return obj.items.count()


class CheckoutSerializer(serializers.Serializer):
    """
    Checkout serializer for processing orders
    """

    shipping_address = serializers.JSONField()
    billing_address = serializers.JSONField()
    shipping_method_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)
    payment_method_id = serializers.IntegerField()

    def validate_shipping_address(self, value):
        """Validate shipping address"""
        required_fields = [
            "first_name",
            "last_name",
            "address_line_1",
            "city",
            "state_province",
            "postal_code",
            "country",
        ]

        for field in required_fields:
            if not value.get(field):
                raise serializers.ValidationError(
                    f"{field} is required in shipping address."
                )

        return value

    def validate_billing_address(self, value):
        """Validate billing address"""
        required_fields = [
            "first_name",
            "last_name",
            "address_line_1",
            "city",
            "state_province",
            "postal_code",
            "country",
        ]

        for field in required_fields:
            if not value.get(field):
                raise serializers.ValidationError(
                    f"{field} is required in billing address."
                )

        return value

    def validate_shipping_method_id(self, value):
        """Validate shipping method"""
        try:
            shipping_method = ShippingMethod.objects.get(id=value, is_active=True)
        except ShippingMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid shipping method.")

        return value

    def validate_payment_method_id(self, value):
        """Validate payment method"""
        from apps.payments.models import PaymentMethod

        try:
            payment_method = PaymentMethod.objects.get(id=value, is_active=True)
        except PaymentMethod.DoesNotExist:
            raise serializers.ValidationError("Invalid payment method.")

        return value

    def validate(self, attrs):
        """Validate checkout data"""
        # Check if cart is not empty
        cart = self.context.get("cart")
        if not cart or cart.is_empty:
            raise serializers.ValidationError("Cart is empty.")

        # Validate cart items
        for item in cart.items.all():
            if not item.is_available:
                raise serializers.ValidationError(
                    f"Product '{item.product_variant.product.name}' is out of stock."
                )

            if item.quantity > item.available_quantity:
                raise serializers.ValidationError(
                    f"Only {item.available_quantity} items available for '{item.product_variant.product.name}'."
                )

        return attrs


class ShippingMethodSerializer(serializers.ModelSerializer):
    """
    Shipping method serializer
    """

    class Meta:
        model = ShippingMethod
        fields = [
            "id",
            "name",
            "description",
            "base_cost",
            "cost_per_kg",
            "estimated_days_min",
            "estimated_days_max",
            "is_digital",
        ]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """
    Order status history serializer
    """

    changed_by_name = serializers.CharField(
        source="changed_by.full_name", read_only=True
    )

    class Meta:
        model = OrderStatusHistory
        fields = [
            "id",
            "status",
            "payment_status",
            "notes",
            "changed_by_name",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Order update serializer for admin/vendor updates
    """

    class Meta:
        model = Order
        fields = [
            "status",
            "payment_status",
            "internal_notes",
        ]

    def validate_status(self, value):
        """Validate status transition"""
        instance = self.instance
        if instance:
            # Define valid status transitions
            valid_transitions = {
                "pending": ["confirmed", "cancelled"],
                "confirmed": ["processing", "cancelled"],
                "processing": ["shipped", "cancelled"],
                "shipped": ["delivered"],
                "delivered": [],
                "cancelled": [],
                "refunded": [],
            }

            current_status = instance.status
            if value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Invalid status transition from {current_status} to {value}."
                )

        return value
