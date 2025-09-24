"""
Payment serializers for NexusCommerce
"""

from rest_framework import serializers

from .models import Payment, PaymentMethod, Refund


class PaymentMethodSerializer(serializers.ModelSerializer):
    """
    Payment method serializer
    """

    class Meta:
        model = PaymentMethod
        fields = [
            "id",
            "name",
            "payment_type",
            "description",
            "is_active",
            "processing_fee_percentage",
            "processing_fee_fixed",
            "min_amount",
            "max_amount",
        ]


class PaymentSerializer(serializers.ModelSerializer):
    """
    Payment serializer
    """

    payment_method_name = serializers.CharField(
        source="payment_method.name", read_only=True
    )
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    customer_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_id",
            "order",
            "order_number",
            "user",
            "customer_name",
            "payment_method",
            "payment_method_name",
            "amount",
            "currency",
            "status",
            "provider_payment_id",
            "processing_fee",
            "failure_reason",
            "notes",
            "created_at",
            "updated_at",
            "processed_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "payment_id",
            "user",
            "provider_payment_id",
            "processing_fee",
            "failure_reason",
            "created_at",
            "updated_at",
            "processed_at",
            "completed_at",
        ]


class PaymentCreateSerializer(serializers.ModelSerializer):
    """
    Payment creation serializer
    """

    class Meta:
        model = Payment
        fields = [
            "order",
            "payment_method",
            "amount",
            "currency",
        ]

    def validate_order(self, value):
        """Validate order"""
        if value.customer != self.context["request"].user:
            raise serializers.ValidationError("You can only pay for your own orders.")

        if value.payment_status == "paid":
            raise serializers.ValidationError("Order is already paid.")

        return value

    def validate_payment_method(self, value):
        """Validate payment method"""
        if not value.is_active:
            raise serializers.ValidationError("Payment method is not active.")

        return value

    def validate_amount(self, value):
        """Validate payment amount"""
        order = self.initial_data.get("order")
        if order:
            order_obj = order
            if value != order_obj.total_amount:
                raise serializers.ValidationError(
                    f"Payment amount must match order total: {order_obj.total_amount}"
                )

        return value


class RefundSerializer(serializers.ModelSerializer):
    """
    Refund serializer
    """

    payment_id = serializers.CharField(source="payment.payment_id", read_only=True)
    order_number = serializers.CharField(source="order.order_number", read_only=True)
    processed_by_name = serializers.CharField(
        source="processed_by.full_name", read_only=True
    )

    class Meta:
        model = Refund
        fields = [
            "id",
            "refund_id",
            "payment",
            "payment_id",
            "order",
            "order_number",
            "amount",
            "currency",
            "status",
            "reason",
            "provider_refund_id",
            "processed_by",
            "processed_by_name",
            "notes",
            "created_at",
            "updated_at",
            "processed_at",
            "completed_at",
        ]
        read_only_fields = [
            "id",
            "refund_id",
            "provider_refund_id",
            "processed_by",
            "created_at",
            "updated_at",
            "processed_at",
            "completed_at",
        ]


class RefundCreateSerializer(serializers.ModelSerializer):
    """
    Refund creation serializer
    """

    class Meta:
        model = Refund
        fields = [
            "payment",
            "amount",
            "reason",
            "notes",
        ]

    def validate_payment(self, value):
        """Validate payment"""
        if not value.is_successful:
            raise serializers.ValidationError("Can only refund successful payments.")

        # Check if payment has already been fully refunded
        total_refunded = sum(
            refund.amount for refund in value.refunds.filter(status="completed")
        )
        if total_refunded >= value.amount:
            raise serializers.ValidationError(
                "Payment has already been fully refunded."
            )

        return value

    def validate_amount(self, value):
        """Validate refund amount"""
        payment = self.initial_data.get("payment")
        if payment:
            # Check if refund amount exceeds available amount
            total_refunded = sum(
                refund.amount for refund in payment.refunds.filter(status="completed")
            )
            available_amount = payment.amount - total_refunded

            if value > available_amount:
                raise serializers.ValidationError(
                    f"Refund amount cannot exceed available amount: {available_amount}"
                )

        return value
