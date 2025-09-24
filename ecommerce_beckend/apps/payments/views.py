"""
Payment views for NexusCommerce
"""

from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdminUser, IsOwnerOrAdmin

from .models import Payment, PaymentMethod, Refund
from .serializers import (PaymentCreateSerializer, PaymentMethodSerializer,
                          PaymentSerializer, RefundCreateSerializer,
                          RefundSerializer)


class PaymentMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Payment method viewset
    """

    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List payment methods",
        description="Get all active payment methods",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Payment viewset
    """

    queryset = Payment.objects.select_related("order", "user", "payment_method")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return PaymentCreateSerializer
        return PaymentSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by user role
        if self.request.user.is_admin:
            return queryset
        else:
            # Users can only see their own payments
            return queryset.filter(user=self.request.user)

    @extend_schema(
        summary="List payments",
        description="Get all payments for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get payment details",
        description="Get detailed information about a specific payment",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create payment",
        description="Create a new payment for an order",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create payment
        payment = serializer.save(user=request.user)

        # Process payment (simplified - in real implementation, integrate with payment gateway)
        payment = self.process_payment(payment)

        return Response(
            {
                "status": "success",
                "data": PaymentSerializer(payment).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def process_payment(self, payment):
        """Process payment (simplified implementation)"""
        # In a real implementation, this would integrate with payment gateways
        # like Stripe, PayPal, etc.

        try:
            # Simulate payment processing
            payment.status = "processing"
            payment.processed_at = timezone.now()
            payment.save()

            # Simulate successful payment
            payment.status = "completed"
            payment.completed_at = timezone.now()
            payment.provider_payment_id = f"PAY_{payment.payment_id}"
            payment.save()

            # Update order payment status
            payment.order.payment_status = "paid"
            payment.order.save()

        except Exception as e:
            # Handle payment failure
            payment.status = "failed"
            payment.failure_reason = str(e)
            payment.save()

            # Update order payment status
            payment.order.payment_status = "failed"
            payment.order.save()

        return payment

    @extend_schema(
        summary="Get my payments",
        description="Get all payments for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )


class RefundViewSet(viewsets.ModelViewSet):
    """
    Refund viewset
    """

    queryset = Refund.objects.select_related("payment", "order", "processed_by")
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return RefundCreateSerializer
        return RefundSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            self.permission_classes = [IsOwnerOrAdmin]
        elif self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by user role
        if self.request.user.is_admin:
            return queryset
        else:
            # Users can only see refunds for their own payments
            return queryset.filter(payment__user=self.request.user)

    @extend_schema(
        summary="List refunds",
        description="Get all refunds for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get refund details",
        description="Get detailed information about a specific refund",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create refund",
        description="Create a new refund for a payment",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create refund
        refund = serializer.save()

        # Process refund (simplified - in real implementation, integrate with payment gateway)
        refund = self.process_refund(refund, request.user)

        return Response(
            {
                "status": "success",
                "data": RefundSerializer(refund).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def process_refund(self, refund, user):
        """Process refund (simplified implementation)"""
        # In a real implementation, this would integrate with payment gateways

        try:
            # Simulate refund processing
            refund.status = "processing"
            refund.processed_by = user
            refund.processed_at = timezone.now()
            refund.save()

            # Simulate successful refund
            refund.status = "completed"
            refund.completed_at = timezone.now()
            refund.provider_refund_id = f"REF_{refund.refund_id}"
            refund.save()

            # Update payment and order status
            payment = refund.payment
            order = refund.order

            # Check if this is a full refund
            total_refunded = sum(
                r.amount for r in payment.refunds.filter(status="completed")
            )
            if total_refunded >= payment.amount:
                payment.order.payment_status = "refunded"
            else:
                payment.order.payment_status = "partially_refunded"

            order.save()

        except Exception as e:
            # Handle refund failure
            refund.status = "failed"
            refund.save()

        return refund

    @extend_schema(
        summary="Get my refunds",
        description="Get all refunds for the current user",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def my_refunds(self, request):
        queryset = self.get_queryset().filter(payment__user=request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )
