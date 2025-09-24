"""
Cart views for NexusCommerce
"""

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem
from .serializers import (AddToCartSerializer, CartItemSerializer,
                          CartSerializer, UpdateCartItemSerializer)


class CartViewSet(viewsets.ModelViewSet):
    """
    Cart viewset for managing user's shopping cart
    """

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        """Get or create cart for the current user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    @extend_schema(
        summary="Get cart",
        description="Get the current user's shopping cart",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Add item to cart",
        description="Add a product variant to the cart",
        request=AddToCartSerializer,
        responses={
            201: CartItemSerializer,
            400: {"description": "Validation error"},
        },
    )
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self.get_object()
        serializer = AddToCartSerializer(data=request.data, context={"cart": cart})
        serializer.is_valid(raise_exception=True)

        product_variant_id = serializer.validated_data["product_variant_id"]
        quantity = serializer.validated_data["quantity"]

        with transaction.atomic():
            # Check if item already exists in cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_variant_id=product_variant_id,
                defaults={"quantity": quantity},
            )

            if not created:
                # Update quantity if item already exists
                new_quantity = cart_item.quantity + quantity
                if new_quantity > cart_item.available_quantity:
                    return Response(
                        {
                            "status": "error",
                            "error": {
                                "message": f"Only {cart_item.available_quantity} items available in stock.",
                            },
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                cart_item.quantity = new_quantity
                cart_item.save()

        return Response(
            {
                "status": "success",
                "data": CartItemSerializer(cart_item).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Remove item from cart",
        description="Remove a product variant from the cart",
        responses={
            204: {"description": "Item removed successfully"},
            404: {"description": "Item not found"},
        },
    )
    @action(
        detail=False,
        methods=["delete"],
        url_path="remove_item/(?P<item_id>[^/.]+)",
    )
    def remove_item(self, request, item_id=None):
        cart = self.get_object()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()

        return Response(
            {
                "status": "success",
                "data": {"message": "Item removed from cart"},
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        summary="Clear cart",
        description="Remove all items from the cart",
        responses={
            200: {"description": "Cart cleared successfully"},
        },
    )
    @action(detail=False, methods=["delete"])
    def clear(self, request):
        cart = self.get_object()
        cart.items.all().delete()

        return Response(
            {
                "status": "success",
                "data": {"message": "Cart cleared successfully"},
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update cart item quantity",
        description="Update the quantity of a cart item",
        request=UpdateCartItemSerializer,
        responses={
            200: CartItemSerializer,
            400: {"description": "Validation error"},
        },
    )
    @action(
        detail=False,
        methods=["patch"],
        url_path="update_item/(?P<item_id>[^/.]+)",
    )
    def update_item(self, request, item_id=None):
        cart = self.get_object()
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        serializer = UpdateCartItemSerializer(
            data=request.data, context={"cart_item": cart_item}
        )
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]

        if quantity == 0:
            cart_item.delete()
            return Response(
                {
                    "status": "success",
                    "data": {"message": "Item removed from cart"},
                },
                status=status.HTTP_200_OK,
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            {
                "status": "success",
                "data": CartItemSerializer(cart_item).data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Validate cart",
        description="Validate cart items for stock availability and pricing",
        responses={
            200: {"description": "Cart validation results"},
        },
    )
    @action(detail=False, methods=["get"])
    def validate(self, request):
        cart = self.get_object()
        validation_results = {
            "is_valid": True,
            "issues": [],
            "updated_items": [],
        }

        for item in cart.items.all():
            item_issues = []

            # Check stock availability
            if not item.is_available:
                item_issues.append("Item is out of stock")
                validation_results["is_valid"] = False

            # Check if quantity exceeds available stock
            if item.quantity > item.available_quantity:
                item_issues.append(
                    f"Quantity exceeds available stock ({item.available_quantity})"
                )
                validation_results["is_valid"] = False

            # Check if price has changed
            if item.unit_price != item.product_variant.price:
                item.unit_price = item.product_variant.price
                item.save()
                validation_results["updated_items"].append(
                    {
                        "item_id": item.id,
                        "old_price": str(item.unit_price),
                        "new_price": str(item.product_variant.price),
                    }
                )

            if item_issues:
                validation_results["issues"].append(
                    {
                        "item_id": item.id,
                        "product_name": item.product_variant.product.name,
                        "issues": item_issues,
                    }
                )

        return Response(
            {
                "status": "success",
                "data": validation_results,
            },
            status=status.HTTP_200_OK,
        )


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Cart item viewset for managing individual cart items
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.get_or_create(user=self.request.user)[0]
        return CartItem.objects.filter(cart=cart)

    @extend_schema(
        summary="List cart items",
        description="Get all items in the current user's cart",
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

    @extend_schema(
        summary="Get cart item",
        description="Get details of a specific cart item",
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
        summary="Update cart item",
        description="Update a cart item's quantity",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateCartItemSerializer(
            data=request.data, context={"cart_item": instance}
        )
        serializer.is_valid(raise_exception=True)

        quantity = serializer.validated_data["quantity"]

        if quantity == 0:
            instance.delete()
            return Response(
                {
                    "status": "success",
                    "data": {"message": "Item removed from cart"},
                },
                status=status.HTTP_200_OK,
            )

        instance.quantity = quantity
        instance.save()

        return Response(
            {
                "status": "success",
                "data": CartItemSerializer(instance).data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Delete cart item",
        description="Remove a cart item",
        responses={204: {"description": "Item removed successfully"}},
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {
                "status": "success",
                "data": {"message": "Item removed from cart"},
            },
            status=status.HTTP_204_NO_CONTENT,
        )
