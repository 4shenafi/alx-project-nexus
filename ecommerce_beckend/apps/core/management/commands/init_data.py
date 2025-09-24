"""
Management command to initialize basic data
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.orders.models import ShippingMethod
from apps.payments.models import PaymentMethod
from apps.products.models import (Brand, Category, ProductAttribute,
                                  ProductAttributeValue, Tag)

User = get_user_model()


class Command(BaseCommand):
    help = "Initialize basic data for the application"

    def handle(self, *args, **options):
        self.stdout.write("Initializing basic data...")

        # Create superuser if it doesn't exist
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                email="admin@nexuscommerce.com",
                username="admin",
                password="admin123",
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write(
                self.style.SUCCESS(
                    "Superuser created: admin@nexuscommerce.com / admin123"
                )
            )

        # Create sample categories
        categories_data = [
            {
                "name": "Electronics",
                "description": "Electronic devices and accessories",
            },
            {"name": "Clothing", "description": "Fashion and apparel"},
            {
                "name": "Home & Garden",
                "description": "Home improvement and garden supplies",
            },
            {
                "name": "Sports",
                "description": "Sports equipment and accessories",
            },
            {
                "name": "Books",
                "description": "Books and educational materials",
            },
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"], defaults=cat_data
            )
            if created:
                self.stdout.write(f"Created category: {category.name}")

        # Create sample brands
        brands_data = [
            {"name": "Apple", "description": "Technology company"},
            {"name": "Nike", "description": "Sports and lifestyle brand"},
            {"name": "Samsung", "description": "Electronics manufacturer"},
            {"name": "Adidas", "description": "Sports and lifestyle brand"},
            {
                "name": "Sony",
                "description": "Electronics and entertainment company",
            },
        ]

        for brand_data in brands_data:
            brand, created = Brand.objects.get_or_create(
                name=brand_data["name"], defaults=brand_data
            )
            if created:
                self.stdout.write(f"Created brand: {brand.name}")

        # Create sample tags
        tags_data = [
            {"name": "New", "color": "#28a745"},
            {"name": "Sale", "color": "#dc3545"},
            {"name": "Featured", "color": "#007bff"},
            {"name": "Popular", "color": "#ffc107"},
            {"name": "Limited Edition", "color": "#6f42c1"},
        ]

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_data["name"], defaults=tag_data
            )
            if created:
                self.stdout.write(f"Created tag: {tag.name}")

        # Create product attributes
        attributes_data = [
            {
                "name": "Color",
                "attribute_type": "select",
                "is_variant": True,
                "is_filterable": True,
            },
            {
                "name": "Size",
                "attribute_type": "select",
                "is_variant": True,
                "is_filterable": True,
            },
            {
                "name": "Material",
                "attribute_type": "select",
                "is_variant": False,
                "is_filterable": True,
            },
            {
                "name": "Weight",
                "attribute_type": "number",
                "is_variant": False,
                "is_filterable": True,
            },
        ]

        for attr_data in attributes_data:
            attribute, created = ProductAttribute.objects.get_or_create(
                name=attr_data["name"], defaults=attr_data
            )
            if created:
                self.stdout.write(f"Created attribute: {attribute.name}")

        # Create attribute values for Color
        color_attribute = ProductAttribute.objects.get(name="Color")
        color_values = [
            "Red",
            "Blue",
            "Green",
            "Black",
            "White",
            "Yellow",
            "Purple",
            "Orange",
        ]
        for color in color_values:
            value, created = ProductAttributeValue.objects.get_or_create(
                attribute=color_attribute, value=color
            )
            if created:
                self.stdout.write(f"Created color value: {color}")

        # Create attribute values for Size
        size_attribute = ProductAttribute.objects.get(name="Size")
        size_values = ["XS", "S", "M", "L", "XL", "XXL"]
        for size in size_values:
            value, created = ProductAttributeValue.objects.get_or_create(
                attribute=size_attribute, value=size
            )
            if created:
                self.stdout.write(f"Created size value: {size}")

        # Create payment methods
        payment_methods_data = [
            {
                "name": "Credit Card",
                "payment_type": "credit_card",
                "description": "Pay with credit card",
                "processing_fee_percentage": 2.9,
                "processing_fee_fixed": 0.30,
            },
            {
                "name": "PayPal",
                "payment_type": "paypal",
                "description": "Pay with PayPal",
                "processing_fee_percentage": 3.4,
                "processing_fee_fixed": 0.35,
            },
            {
                "name": "Bank Transfer",
                "payment_type": "bank_transfer",
                "description": "Direct bank transfer",
                "processing_fee_percentage": 0.0,
                "processing_fee_fixed": 0.0,
            },
        ]

        for pm_data in payment_methods_data:
            payment_method, created = PaymentMethod.objects.get_or_create(
                name=pm_data["name"], defaults=pm_data
            )
            if created:
                self.stdout.write(f"Created payment method: {payment_method.name}")

        # Create shipping methods
        shipping_methods_data = [
            {
                "name": "Standard Shipping",
                "description": "Standard ground shipping",
                "base_cost": 5.99,
                "cost_per_kg": 1.50,
                "estimated_days_min": 3,
                "estimated_days_max": 7,
            },
            {
                "name": "Express Shipping",
                "description": "Express 2-day shipping",
                "base_cost": 12.99,
                "cost_per_kg": 2.50,
                "estimated_days_min": 1,
                "estimated_days_max": 2,
            },
            {
                "name": "Overnight Shipping",
                "description": "Next day delivery",
                "base_cost": 24.99,
                "cost_per_kg": 5.00,
                "estimated_days_min": 1,
                "estimated_days_max": 1,
            },
        ]

        for sm_data in shipping_methods_data:
            shipping_method, created = ShippingMethod.objects.get_or_create(
                name=sm_data["name"], defaults=sm_data
            )
            if created:
                self.stdout.write(f"Created shipping method: {shipping_method.name}")

        self.stdout.write(self.style.SUCCESS("Successfully initialized basic data!"))
