"""
Product models for NexusCommerce
"""

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Category(models.Model):
    """
    Product category model with hierarchical structure
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        db_index=True,
    )
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        help_text="Category image",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["parent"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def full_path(self):
        """Get the full category path"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name


class Brand(models.Model):
    """
    Product brand model
    """

    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="brands/", blank=True, null=True, help_text="Brand logo"
    )
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "brands"
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Product tag model for flexible categorization
    """

    name = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=60, unique=True, db_index=True)
    color = models.CharField(
        max_length=7, default="#007bff", help_text="Hex color code for the tag"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tags"
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Main product model
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("discontinued", "Discontinued"),
    ]

    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=300, unique=True, db_index=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True, null=True)
    sku = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Stock Keeping Unit",
    )
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"role": "vendor"},
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        db_index=True,
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
        db_index=True,
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", db_index=True
    )
    is_featured = models.BooleanField(default=False, db_index=True)
    is_digital = models.BooleanField(
        default=False, help_text="Whether this is a digital product"
    )
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg",
    )
    dimensions = models.JSONField(
        default=dict,
        blank=True,
        help_text="Product dimensions (length, width, height)",
    )
    seo_title = models.CharField(max_length=60, blank=True, null=True)
    seo_description = models.CharField(max_length=160, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_featured"]),
            models.Index(fields=["vendor"]),
            models.Index(fields=["category"]),
            models.Index(fields=["brand"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        """Get the primary product image"""
        return self.images.filter(is_primary=True).first()

    @property
    def min_price(self):
        """Get the minimum price among all variants"""
        variants = self.variants.filter(is_active=True)
        if variants.exists():
            return min(variant.price for variant in variants)
        return None

    @property
    def max_price(self):
        """Get the maximum price among all variants"""
        variants = self.variants.filter(is_active=True)
        if variants.exists():
            return max(variant.price for variant in variants)
        return None


class ProductAttribute(models.Model):
    """
    Product attribute model (e.g., Color, Size, Material)
    """

    ATTRIBUTE_TYPE_CHOICES = [
        ("text", "Text"),
        ("number", "Number"),
        ("select", "Select"),
        ("multiselect", "Multi-Select"),
        ("boolean", "Boolean"),
    ]

    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(max_length=120, unique=True, db_index=True)
    attribute_type = models.CharField(
        max_length=20, choices=ATTRIBUTE_TYPE_CHOICES, default="text"
    )
    is_required = models.BooleanField(default=False)
    is_variant = models.BooleanField(
        default=False,
        help_text="Whether this attribute creates product variants",
    )
    is_filterable = models.BooleanField(
        default=True,
        help_text="Whether this attribute can be used for filtering",
    )
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_attributes"
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"
        ordering = ["sort_order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_variant"]),
            models.Index(fields=["is_filterable"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductAttributeValue(models.Model):
    """
    Product attribute value model
    """

    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="values",
        db_index=True,
    )
    value = models.CharField(max_length=255, db_index=True)
    display_value = models.CharField(max_length=255, blank=True, null=True)
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_attribute_values"
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"
        ordering = ["sort_order", "value"]
        unique_together = [["attribute", "value"]]
        indexes = [
            models.Index(fields=["attribute", "value"]),
        ]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariant(models.Model):
    """
    Product variant model - the canonical purchasable entity
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        db_index=True,
    )
    sku = models.CharField(
        max_length=100, unique=True, db_index=True, help_text="Variant SKU"
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True,
    )
    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Original price for comparison",
    )
    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Cost price for profit calculation",
    )
    stock_quantity = models.PositiveIntegerField(
        default=0, db_index=True, help_text="Available stock quantity"
    )
    low_stock_threshold = models.PositiveIntegerField(
        default=5, help_text="Threshold for low stock alerts"
    )
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Variant weight in kg",
    )
    is_active = models.BooleanField(default=True, db_index=True)
    is_digital = models.BooleanField(
        default=False, help_text="Whether this variant is digital"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_variants"
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["price"]),
            models.Index(fields=["stock_quantity"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["product", "is_active"]),
        ]

    def __str__(self):
        if self.name:
            return f"{self.product.name} - {self.name}"
        return f"{self.product.name} - {self.sku}"

    @property
    def is_in_stock(self):
        """Check if variant is in stock"""
        return self.stock_quantity > 0

    @property
    def is_low_stock(self):
        """Check if variant is low in stock"""
        return self.stock_quantity <= self.low_stock_threshold

    @property
    def discount_percentage(self):
        """Calculate discount percentage if compare_at_price is set"""
        if self.compare_at_price and self.compare_at_price > self.price:
            return round(
                ((self.compare_at_price - self.price) / self.compare_at_price) * 100,
                2,
            )
        return 0


class ProductVariantAttribute(models.Model):
    """
    Product variant attribute mapping
    """

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
        db_index=True,
    )
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, db_index=True
    )
    value = models.ForeignKey(
        ProductAttributeValue, on_delete=models.CASCADE, db_index=True
    )

    class Meta:
        db_table = "product_variant_attributes"
        verbose_name = "Product Variant Attribute"
        verbose_name_plural = "Product Variant Attributes"
        unique_together = [["variant", "attribute"]]
        indexes = [
            models.Index(fields=["variant", "attribute"]),
        ]

    def __str__(self):
        return f"{self.variant} - {self.attribute.name}: {self.value.value}"


class ProductImage(models.Model):
    """
    Product image model
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", db_index=True
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True,
        db_index=True,
    )
    image = models.ImageField(upload_to="products/", help_text="Product image")
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Alternative text for accessibility",
    )
    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this is the primary image",
    )
    sort_order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_images"
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["sort_order", "created_at"]
        indexes = [
            models.Index(fields=["product", "is_primary"]),
            models.Index(fields=["variant"]),
        ]

    def __str__(self):
        return f"{self.product.name} - Image {self.id}"

    def save(self, *args, **kwargs):
        # Ensure only one primary image per product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductReview(models.Model):
    """
    Product review model
    """

    RATING_CHOICES = [
        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        db_index=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews", db_index=True
    )
    rating = models.PositiveIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        db_index=True,
    )
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(
        default=False,
        help_text="Whether this review is from a verified purchase",
    )
    is_approved = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this review is approved for display",
    )
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product_reviews"
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ["-created_at"]
        unique_together = [["product", "user"]]
        indexes = [
            models.Index(fields=["product", "is_approved"]),
            models.Index(fields=["rating"]),
            models.Index(fields=["is_verified_purchase"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.user.email} ({self.rating} stars)"
