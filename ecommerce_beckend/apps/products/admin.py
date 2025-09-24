"""
Admin configuration for products app
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (Brand, Category, Product, ProductAttribute,
                     ProductAttributeValue, ProductImage, ProductReview,
                     ProductVariant, ProductVariantAttribute, Tag)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Category admin
    """

    list_display = [
        "name",
        "slug",
        "parent",
        "is_active",
        "sort_order",
        "created_at",
    ]
    list_filter = ["is_active", "parent", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Brand admin
    """

    list_display = ["name", "slug", "is_active", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Tag admin
    """

    list_display = ["name", "slug", "color_display", "created_at"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]

    def color_display(self, obj):
        return format_html('<span style="color: {};">●</span> {}', obj.color, obj.color)

    color_display.short_description = "Color"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Product admin
    """

    list_display = [
        "name",
        "sku",
        "vendor",
        "category",
        "brand",
        "status",
        "is_featured",
        "min_price_display",
        "created_at",
    ]
    list_filter = [
        "status",
        "is_featured",
        "is_digital",
        "category",
        "brand",
        "vendor",
        "created_at",
    ]
    search_fields = ["name", "sku", "description"]
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ["tags"]
    ordering = ["-created_at"]

    def min_price_display(self, obj):
        min_price = obj.min_price
        return f"${min_price}" if min_price else "N/A"

    min_price_display.short_description = "Min Price"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """
    ProductVariant admin
    """

    list_display = [
        "product",
        "sku",
        "name",
        "price",
        "stock_quantity",
        "is_active",
        "is_in_stock_display",
        "created_at",
    ]
    list_filter = ["is_active", "is_digital", "product__vendor", "created_at"]
    search_fields = ["sku", "name", "product__name"]
    ordering = ["-created_at"]

    def is_in_stock_display(self, obj):
        if obj.is_in_stock:
            return format_html('<span style="color: green;">✓ In Stock</span>')
        else:
            return format_html('<span style="color: red;">✗ Out of Stock</span>')

    is_in_stock_display.short_description = "Stock Status"


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """
    ProductAttribute admin
    """

    list_display = [
        "name",
        "slug",
        "attribute_type",
        "is_variant",
        "is_filterable",
        "sort_order",
    ]
    list_filter = ["attribute_type", "is_variant", "is_filterable"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["sort_order", "name"]


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """
    ProductAttributeValue admin
    """

    list_display = ["attribute", "value", "display_value", "sort_order"]
    list_filter = ["attribute"]
    search_fields = ["value", "display_value"]
    ordering = ["attribute", "sort_order", "value"]


@admin.register(ProductVariantAttribute)
class ProductVariantAttributeAdmin(admin.ModelAdmin):
    """
    ProductVariantAttribute admin
    """

    list_display = ["variant", "attribute", "value"]
    list_filter = ["attribute"]
    search_fields = ["variant__sku", "attribute__name", "value__value"]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    ProductImage admin
    """

    list_display = [
        "product",
        "image_display",
        "is_primary",
        "sort_order",
        "created_at",
    ]
    list_filter = ["is_primary", "created_at"]
    search_fields = ["product__name", "alt_text"]
    ordering = ["product", "sort_order"]

    def image_display(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url,
            )
        return "No Image"

    image_display.short_description = "Image"


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """
    ProductReview admin
    """

    list_display = [
        "product",
        "user",
        "rating_display",
        "title",
        "is_verified_purchase",
        "is_approved",
        "helpful_count",
        "created_at",
    ]
    list_filter = [
        "rating",
        "is_verified_purchase",
        "is_approved",
        "created_at",
    ]
    search_fields = ["product__name", "user__email", "title", "comment"]
    ordering = ["-created_at"]

    def rating_display(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)

    rating_display.short_description = "Rating"
