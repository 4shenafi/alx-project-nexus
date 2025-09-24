"""
Product serializers for NexusCommerce
"""

from django.db import transaction
from rest_framework import serializers

from .models import (Brand, Category, Product, ProductAttribute,
                     ProductAttributeValue, ProductImage, ProductReview,
                     ProductVariant, ProductVariantAttribute, Tag)


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer
    """

    children = serializers.SerializerMethodField()
    full_path = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "parent",
            "image",
            "is_active",
            "sort_order",
            "children",
            "full_path",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(obj.children.all(), many=True).data
        return []


class BrandSerializer(serializers.ModelSerializer):
    """
    Brand serializer
    """

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "logo",
            "website",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class TagSerializer(serializers.ModelSerializer):
    """
    Tag serializer
    """

    class Meta:
        model = Tag
        fields = [
            "id",
            "name",
            "slug",
            "color",
            "created_at",
        ]
        read_only_fields = ["id", "slug", "created_at"]


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """
    Product attribute value serializer
    """

    class Meta:
        model = ProductAttributeValue
        fields = ["id", "value", "display_value", "sort_order"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    """
    Product attribute serializer
    """

    values = ProductAttributeValueSerializer(many=True, read_only=True)

    class Meta:
        model = ProductAttribute
        fields = [
            "id",
            "name",
            "slug",
            "attribute_type",
            "is_required",
            "is_variant",
            "is_filterable",
            "sort_order",
            "values",
        ]
        read_only_fields = ["id", "slug"]


class ProductVariantAttributeSerializer(serializers.ModelSerializer):
    """
    Product variant attribute serializer
    """

    attribute_name = serializers.CharField(source="attribute.name", read_only=True)
    value_name = serializers.CharField(source="value.value", read_only=True)

    class Meta:
        model = ProductVariantAttribute
        fields = ["attribute", "attribute_name", "value", "value_name"]


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Product variant serializer
    """

    attributes = ProductVariantAttributeSerializer(many=True, read_only=True)
    is_in_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "name",
            "price",
            "compare_at_price",
            "cost_price",
            "stock_quantity",
            "low_stock_threshold",
            "weight",
            "is_active",
            "is_digital",
            "attributes",
            "is_in_stock",
            "is_low_stock",
            "discount_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Product image serializer
    """

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "alt_text",
            "is_primary",
            "sort_order",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class ProductReviewSerializer(serializers.ModelSerializer):
    """
    Product review serializer
    """

    user_name = serializers.CharField(source="user.full_name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = ProductReview
        fields = [
            "id",
            "user",
            "user_name",
            "user_email",
            "rating",
            "title",
            "comment",
            "is_verified_purchase",
            "is_approved",
            "helpful_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "is_verified_purchase",
            "is_approved",
            "helpful_count",
            "created_at",
            "updated_at",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    """
    Product list serializer for listing views
    """

    primary_image = ProductImageSerializer(read_only=True)
    min_price = serializers.ReadOnlyField()
    max_price = serializers.ReadOnlyField()
    vendor_name = serializers.CharField(source="vendor.full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "short_description",
            "sku",
            "vendor_name",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "tags",
            "status",
            "is_featured",
            "is_digital",
            "primary_image",
            "min_price",
            "max_price",
            "created_at",
            "updated_at",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Product detail serializer for detailed views
    """

    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    vendor_name = serializers.CharField(source="vendor.full_name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    min_price = serializers.ReadOnlyField()
    max_price = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "short_description",
            "sku",
            "vendor",
            "vendor_name",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "tags",
            "status",
            "is_featured",
            "is_digital",
            "weight",
            "dimensions",
            "seo_title",
            "seo_description",
            "variants",
            "images",
            "reviews",
            "min_price",
            "max_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Product create/update serializer with nested writes
    """

    variants = ProductVariantSerializer(many=True, required=False)
    images = ProductImageSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "short_description",
            "sku",
            "category",
            "brand",
            "tags",
            "status",
            "is_featured",
            "is_digital",
            "weight",
            "dimensions",
            "seo_title",
            "seo_description",
            "variants",
            "images",
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop("variants", [])
        images_data = validated_data.pop("images", [])
        tags_data = validated_data.pop("tags", [])

        with transaction.atomic():
            # Create product
            product = Product.objects.create(**validated_data)

            # Add tags
            product.tags.set(tags_data)

            # Create variants
            for variant_data in variants_data:
                ProductVariant.objects.create(product=product, **variant_data)

            # Create images
            for image_data in images_data:
                ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        variants_data = validated_data.pop("variants", [])
        images_data = validated_data.pop("images", [])
        tags_data = validated_data.pop("tags", [])

        with transaction.atomic():
            # Update product
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Update tags
            if tags_data is not None:
                instance.tags.set(tags_data)

            # Update variants
            if variants_data is not None:
                # Delete existing variants
                instance.variants.all().delete()
                # Create new variants
                for variant_data in variants_data:
                    ProductVariant.objects.create(product=instance, **variant_data)

            # Update images
            if images_data is not None:
                # Delete existing images
                instance.images.all().delete()
                # Create new images
                for image_data in images_data:
                    ProductImage.objects.create(product=instance, **image_data)

        return instance


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    """
    Product review creation serializer
    """

    class Meta:
        model = ProductReview
        fields = ["rating", "title", "comment"]

    def create(self, validated_data):
        product = self.context["product"]
        user = self.context["request"].user

        # Check if user already reviewed this product
        if ProductReview.objects.filter(product=product, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")

        # Check if user has purchased this product (for verified purchase)
        has_purchased = False
        # This would need to be implemented based on order history

        validated_data.update(
            {
                "product": product,
                "user": user,
                "is_verified_purchase": has_purchased,
            }
        )

        return super().create(validated_data)
