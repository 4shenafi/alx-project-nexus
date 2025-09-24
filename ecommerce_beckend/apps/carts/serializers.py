"""
Cart serializers for NexusCommerce
"""

from decimal import Decimal

from rest_framework import serializers

from apps.products.serializers import ProductVariantSerializer

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    """
    Cart item serializer
    """

    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.IntegerField(write_only=True)
    product_name = serializers.CharField(
        source="product_variant.product.name", read_only=True
    )
    variant_name = serializers.CharField(source="product_variant.name", read_only=True)
    is_available = serializers.ReadOnlyField()
    available_quantity = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product_variant",
            "product_variant_id",
            "product_name",
            "variant_name",
            "quantity",
            "unit_price",
            "total_price",
            "is_available",
            "available_quantity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "product_variant",
            "unit_price",
            "total_price",
            "created_at",
            "updated_at",
        ]

    def validate_product_variant_id(self, value):
        """Validate that the product variant exists and is active"""
        from apps.products.models import ProductVariant

        try:
            variant = ProductVariant.objects.get(id=value, is_active=True)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Product variant not found or inactive.")

        return value

    def validate_quantity(self, value):
        """Validate quantity"""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        return value

    def validate(self, attrs):
        """Validate cart item"""
        product_variant_id = attrs.get("product_variant_id")
        quantity = attrs.get("quantity")

        if product_variant_id and quantity:
            from apps.products.models import ProductVariant

            variant = ProductVariant.objects.get(id=product_variant_id)

            # Check stock availability
            if variant.stock_quantity < quantity:
                raise serializers.ValidationError(
                    f"Only {variant.stock_quantity} items available in stock."
                )

            # Check if variant is digital and user already has it
            if variant.is_digital:
                cart = self.context.get("cart")
                if cart and cart.items.filter(product_variant=variant).exists():
                    raise serializers.ValidationError(
                        "Digital product already in cart."
                    )

        return attrs


class CartSerializer(serializers.ModelSerializer):
    """
    Cart serializer
    """

    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.ReadOnlyField()
    subtotal = serializers.ReadOnlyField()
    is_empty = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "is_empty",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding items to cart
    """

    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_variant_id(self, value):
        """Validate that the product variant exists and is active"""
        from apps.products.models import ProductVariant

        try:
            variant = ProductVariant.objects.get(id=value, is_active=True)
        except ProductVariant.DoesNotExist:
            raise serializers.ValidationError("Product variant not found or inactive.")

        return value

    def validate(self, attrs):
        """Validate add to cart request"""
        product_variant_id = attrs.get("product_variant_id")
        quantity = attrs.get("quantity")

        from apps.products.models import ProductVariant

        variant = ProductVariant.objects.get(id=product_variant_id)

        # Check stock availability
        if variant.stock_quantity < quantity:
            raise serializers.ValidationError(
                f"Only {variant.stock_quantity} items available in stock."
            )

        # Check if variant is digital and user already has it
        if variant.is_digital:
            cart = self.context.get("cart")
            if cart and cart.items.filter(product_variant=variant).exists():
                raise serializers.ValidationError("Digital product already in cart.")

        return attrs


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer for updating cart item quantity
    """

    quantity = serializers.IntegerField(min_value=1)

    def validate_quantity(self, value):
        """Validate quantity against available stock"""
        cart_item = self.context.get("cart_item")
        if cart_item:
            if value > cart_item.available_quantity:
                raise serializers.ValidationError(
                    f"Only {cart_item.available_quantity} items available in stock."
                )
        return value
