"""
Order views for NexusCommerce
"""

from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.carts.models import Cart, CartItem
from apps.payments.models import PaymentMethod
from apps.products.models import ProductVariant
from apps.users.permissions import IsOwnerOrAdmin, IsVendorOwnerOrAdmin

from .models import (Order, OrderItem, OrderShipping, OrderStatusHistory,
                     ShippingMethod)
from .serializers import (CheckoutSerializer, OrderItemSerializer,
                          OrderListSerializer, OrderSerializer,
                          OrderStatusHistorySerializer, OrderUpdateSerializer,
                          ShippingMethodSerializer)


class ShippingMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Shipping method viewset
    """

    queryset = ShippingMethod.objects.filter(is_active=True)
    serializer_class = ShippingMethodSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List shipping methods",
        description="Get all active shipping methods",
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


class OrderViewSet(viewsets.ModelViewSet):
    """
    Order viewset with full CRUD operations
    """

    queryset = Order.objects.select_related("customer").prefetch_related(
        "items", "shipping"
    )
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action in ["update", "partial_update"]:
            return OrderUpdateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsVendorOwnerOrAdmin]
        elif self.action in ["my_orders"]:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by user role
        if self.request.user.is_admin:
            return queryset
        elif self.request.user.is_vendor:
            # Vendors can see orders for their products
            return queryset.filter(
                items__product_variant__product__vendor=self.request.user
            ).distinct()
        else:
            # Customers can only see their own orders
            return queryset.filter(customer=self.request.user)

    @extend_schema(
        summary="List orders",
        description="Get all orders for the current user",
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
        summary="Get order details",
        description="Get detailed information about a specific order",
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
        summary="Get my orders",
        description="Get all orders for the current customer",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def my_orders(self, request):
        queryset = self.get_queryset().filter(customer=request.user)
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

    @extend_schema(
        summary="Update order status",
        description="Update order status (admin/vendor only)",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Create status history entry
        old_status = instance.status
        old_payment_status = instance.payment_status

        order = serializer.save()

        # Record status change
        if old_status != order.status or old_payment_status != order.payment_status:
            OrderStatusHistory.objects.create(
                order=order,
                status=order.status,
                payment_status=order.payment_status,
                notes=request.data.get("status_notes", ""),
                changed_by=request.user,
            )

        return Response(
            {
                "status": "success",
                "data": OrderSerializer(order).data,
            }
        )


class CheckoutView(generics.GenericAPIView):
    """
    Checkout view for processing orders
    """

    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Process checkout",
        description="Process checkout and create order from cart",
        responses={
            201: OrderSerializer,
            400: {"description": "Validation error"},
        },
    )
    def post(self, request, *args, **kwargs):
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        if cart.is_empty:
            return Response(
                {
                    "status": "error",
                    "error": {"message": "Cart is empty"},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data, context={"cart": cart})
        serializer.is_valid(raise_exception=True)

        # Process checkout
        order = self.process_checkout(cart, serializer.validated_data, request.user)

        return Response(
            {
                "status": "success",
                "data": OrderSerializer(order).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def process_checkout(self, cart, validated_data, user):
        """Process the checkout and create order"""
        with transaction.atomic():
            # Create order
            order = Order.objects.create(
                customer=user,
                shipping_address=validated_data["shipping_address"],
                billing_address=validated_data["billing_address"],
                notes=validated_data.get("notes", ""),
            )

            # Calculate totals
            subtotal = Decimal("0.00")

            # Create order items and calculate subtotal
            for cart_item in cart.items.all():
                # Lock the product variant to prevent race conditions
                variant = ProductVariant.objects.select_for_update().get(
                    id=cart_item.product_variant.id
                )

                # Double-check stock availability
                if variant.stock_quantity < cart_item.quantity:
                    raise ValueError(f"Insufficient stock for {variant.product.name}")

                # Create order item
                order_item = OrderItem.objects.create(
                    order=order,
                    product_variant_id=variant.id,
                    product_name=variant.product.name,
                    variant_name=variant.name,
                    sku=variant.sku,
                    unit_price=variant.price,
                    quantity=cart_item.quantity,
                    product_attributes=self.get_variant_attributes(variant),
                )

                # Update stock
                variant.stock_quantity -= cart_item.quantity
                variant.save()

                subtotal += order_item.total_price

            # Get shipping method
            shipping_method = ShippingMethod.objects.get(
                id=validated_data["shipping_method_id"]
            )

            # Calculate shipping cost
            shipping_cost = self.calculate_shipping_cost(cart, shipping_method)

            # Calculate tax (simplified - 10% of subtotal)
            tax_amount = subtotal * Decimal("0.10")

            # Calculate total
            total_amount = subtotal + shipping_cost + tax_amount

            # Update order with calculated amounts
            order.subtotal = subtotal
            order.shipping_amount = shipping_cost
            order.tax_amount = tax_amount
            order.total_amount = total_amount
            order.save()

            # Create shipping record
            OrderShipping.objects.create(
                order=order,
                shipping_method=shipping_method,
                shipping_cost=shipping_cost,
                estimated_delivery=self.calculate_estimated_delivery(shipping_method),
            )

            # Create initial status history
            OrderStatusHistory.objects.create(
                order=order,
                status=order.status,
                payment_status=order.payment_status,
                notes="Order created",
                changed_by=user,
            )

            # Clear cart
            cart.items.all().delete()

            return order

    def get_variant_attributes(self, variant):
        """Get variant attributes as JSON"""
        attributes = {}
        for attr in variant.attributes.all():
            attributes[attr.attribute.name] = attr.value.value
        return attributes

    def calculate_shipping_cost(self, cart, shipping_method):
        """Calculate shipping cost based on cart weight and shipping method"""
        total_weight = Decimal("0.00")

        for item in cart.items.all():
            if item.product_variant.weight:
                total_weight += item.product_variant.weight * item.quantity

        # Calculate cost: base cost + (weight * cost per kg)
        shipping_cost = shipping_method.base_cost + (
            total_weight * shipping_method.cost_per_kg
        )

        return shipping_cost

    def calculate_estimated_delivery(self, shipping_method):
        """Calculate estimated delivery date"""
        from datetime import timedelta

        delivery_days = shipping_method.estimated_days_max
        return timezone.now() + timedelta(days=delivery_days)


class OrderStatusHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Order status history viewset
    """

    serializer_class = OrderStatusHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get("order_pk")
        return OrderStatusHistory.objects.filter(order_id=order_id).order_by(
            "-created_at"
        )

    @extend_schema(
        summary="List order status history",
        description="Get status history for a specific order",
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
