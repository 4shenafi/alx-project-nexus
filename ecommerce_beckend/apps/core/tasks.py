"""
Celery tasks for NexusCommerce
"""

import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task
def send_transactional_email(email_type, user_id, **kwargs):
    """
    Send transactional emails (welcome, OTP, order confirmation, etc.)
    """
    from django.contrib.auth import get_user_model

    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return False

    email_templates = {
        "welcome": {
            "subject": "Welcome to NexusCommerce!",
            "template": "emails/welcome.html",
        },
        "email_verification": {
            "subject": "Verify your email address",
            "template": "emails/email_verification.html",
        },
        "password_reset": {
            "subject": "Reset your password",
            "template": "emails/password_reset.html",
        },
        "order_confirmation": {
            "subject": "Order Confirmation - {order_number}",
            "template": "emails/order_confirmation.html",
        },
        "order_shipped": {
            "subject": "Your order has been shipped - {order_number}",
            "template": "emails/order_shipped.html",
        },
        "order_delivered": {
            "subject": "Your order has been delivered - {order_number}",
            "template": "emails/order_delivered.html",
        },
        "payment_confirmation": {
            "subject": "Payment Confirmation - {order_number}",
            "template": "emails/payment_confirmation.html",
        },
        "low_stock_alert": {
            "subject": "Low Stock Alert - {product_name}",
            "template": "emails/low_stock_alert.html",
        },
    }

    if email_type not in email_templates:
        logger.error(f"Unknown email type: {email_type}")
        return False

    template_info = email_templates[email_type]
    subject = template_info["subject"].format(**kwargs)

    try:
        # Render email template
        context = {"user": user, "site_url": settings.FRONTEND_URL, **kwargs}

        html_message = render_to_string(template_info["template"], context)

        # Send email
        send_mail(
            subject=subject,
            message="",  # Plain text version
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        logger.info(f"Email sent successfully: {email_type} to {user.email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email {email_type} to {user.email}: {str(e)}")
        return False


@shared_task
def generate_image_thumbnails(image_id):
    """
    Generate thumbnails for product images
    """
    import os

    from PIL import Image

    from apps.products.models import ProductImage

    try:
        product_image = ProductImage.objects.get(id=image_id)
    except ProductImage.DoesNotExist:
        logger.error(f"ProductImage with id {image_id} not found")
        return False

    try:
        # Open the original image
        image_path = product_image.image.path
        image = Image.open(image_path)

        # Define thumbnail sizes
        thumbnail_sizes = [
            (150, 150),  # Small thumbnail
            (300, 300),  # Medium thumbnail
            (600, 600),  # Large thumbnail
        ]

        # Generate thumbnails
        for size in thumbnail_sizes:
            thumbnail = image.copy()
            thumbnail.thumbnail(size, Image.Resampling.LANCZOS)

            # Save thumbnail
            thumbnail_name = f"thumb_{size[0]}x{size[1]}_{os.path.basename(image_path)}"
            thumbnail_path = os.path.join(
                os.path.dirname(image_path), "thumbnails", thumbnail_name
            )

            # Create thumbnails directory if it doesn't exist
            os.makedirs(os.path.dirname(thumbnail_path), exist_ok=True)

            thumbnail.save(thumbnail_path, "JPEG", quality=85)

        logger.info(f"Thumbnails generated for image {image_id}")
        return True

    except Exception as e:
        logger.error(f"Failed to generate thumbnails for image {image_id}: {str(e)}")
        return False


@shared_task
def generate_monthly_vendor_report(vendor_id, year, month):
    """
    Generate monthly sales report for vendors
    """
    from apps.orders.models import Order, OrderItem
    from apps.products.models import Product
    from apps.users.models import User

    try:
        vendor = User.objects.get(id=vendor_id, role="vendor")
    except User.DoesNotExist:
        logger.error(f"Vendor with id {vendor_id} not found")
        return False

    try:
        # Calculate date range
        start_date = timezone.datetime(year, month, 1)
        if month == 12:
            end_date = timezone.datetime(year + 1, 1, 1)
        else:
            end_date = timezone.datetime(year, month + 1, 1)

        # Get vendor's products
        vendor_products = Product.objects.filter(vendor=vendor)
        product_ids = vendor_products.values_list("id", flat=True)

        # Get orders for vendor's products in the specified month
        orders = Order.objects.filter(
            items__product_variant__product__in=product_ids,
            created_at__gte=start_date,
            created_at__lt=end_date,
            payment_status="paid",
        ).distinct()

        # Calculate sales metrics
        total_orders = orders.count()
        total_revenue = 0
        total_items_sold = 0
        product_sales = {}

        for order in orders:
            order_items = order.items.filter(product_variant__product__in=product_ids)

            for item in order_items:
                product = item.product_variant.product
                revenue = item.total_price

                total_revenue += revenue
                total_items_sold += item.quantity

                if product.id not in product_sales:
                    product_sales[product.id] = {
                        "product_name": product.name,
                        "quantity_sold": 0,
                        "revenue": 0,
                    }

                product_sales[product.id]["quantity_sold"] += item.quantity
                product_sales[product.id]["revenue"] += revenue

        # Prepare report data
        report_data = {
            "vendor": {
                "id": vendor.id,
                "name": vendor.full_name,
                "email": vendor.email,
            },
            "period": {
                "year": year,
                "month": month,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
            "metrics": {
                "total_orders": total_orders,
                "total_revenue": float(total_revenue),
                "total_items_sold": total_items_sold,
                "average_order_value": float(total_revenue / total_orders)
                if total_orders > 0
                else 0,
            },
            "product_sales": list(product_sales.values()),
        }

        # Send report via email
        send_transactional_email(
            "vendor_report",
            vendor_id,
            report_data=report_data,
            month_name=start_date.strftime("%B"),
            year=year,
        )

        logger.info(f"Monthly report generated for vendor {vendor_id} - {year}/{month}")
        return True

    except Exception as e:
        logger.error(
            f"Failed to generate monthly report for vendor {vendor_id}: {str(e)}"
        )
        return False


@shared_task
def cleanup_expired_sessions():
    """
    Clean up expired user sessions
    """
    from django.contrib.sessions.models import Session

    try:
        # Delete expired sessions
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()

        logger.info(f"Cleaned up {count} expired sessions")
        return count

    except Exception as e:
        logger.error(f"Failed to cleanup expired sessions: {str(e)}")
        return 0


@shared_task
def send_low_stock_alerts():
    """
    Send low stock alerts to vendors
    """
    from apps.products.models import ProductVariant

    try:
        # Get variants with low stock
        from django.db import models

        low_stock_variants = ProductVariant.objects.filter(
            stock_quantity__lte=models.F("low_stock_threshold"), is_active=True
        ).select_related("product__vendor")

        alerts_sent = 0

        for variant in low_stock_variants:
            vendor = variant.product.vendor

            # Send alert to vendor
            send_transactional_email(
                "low_stock_alert",
                vendor.id,
                product_name=variant.product.name,
                variant_name=variant.name,
                current_stock=variant.stock_quantity,
                low_stock_threshold=variant.low_stock_threshold,
            )

            alerts_sent += 1

        logger.info(f"Sent {alerts_sent} low stock alerts")
        return alerts_sent

    except Exception as e:
        logger.error(f"Failed to send low stock alerts: {str(e)}")
        return 0


@shared_task
def update_product_search_index():
    """
    Update product search index (for full-text search)
    """
    from django.db import connection

    from apps.products.models import Product

    try:
        # This is a simplified implementation
        # In a real application, you might use Elasticsearch or similar

        with connection.cursor() as cursor:
            # Update search index for all products
            cursor.execute(
                """
                UPDATE products
                SET search_vector = to_tsvector('english',
                    COALESCE(name, '') || ' ' ||
                    COALESCE(description, '') || ' ' ||
                    COALESCE(short_description, '') || ' ' ||
                    COALESCE(sku, '')
                )
                WHERE status = 'active'
            """
            )

            updated_count = cursor.rowcount

        logger.info(f"Updated search index for {updated_count} products")
        return updated_count

    except Exception as e:
        logger.error(f"Failed to update product search index: {str(e)}")
        return 0


@shared_task
def process_order_fulfillment(order_id):
    """
    Process order fulfillment (inventory updates, notifications, etc.)
    """
    from apps.orders.models import Order

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found")
        return False

    try:
        # Update inventory
        for item in order.items.all():
            variant = item.product_variant
            variant.stock_quantity -= item.quantity
            variant.save()

        # Send order confirmation email
        send_transactional_email(
            "order_confirmation",
            order.customer.id,
            order_number=order.order_number,
            order=order,
        )

        # Update order status
        order.status = "confirmed"
        order.confirmed_at = timezone.now()
        order.save()

        logger.info(f"Order fulfillment processed for order {order_id}")
        return True

    except Exception as e:
        logger.error(
            f"Failed to process order fulfillment for order {order_id}: {str(e)}"
        )
        return False


@shared_task
def process_pending_orders():
    """
    Process pending orders (check for payment confirmation, update status, etc.)
    """
    from apps.orders.models import Order

    try:
        # Get orders that are pending payment confirmation
        pending_orders = Order.objects.filter(
            status="pending",
            payment_status="pending",
            created_at__lt=timezone.now()
            - timedelta(minutes=5),  # Orders older than 5 minutes
        )

        processed_count = 0

        for order in pending_orders:
            # Check if payment has been confirmed
            if order.payment_status == "paid":
                # Process the order fulfillment
                process_order_fulfillment.delay(order.id)
                processed_count += 1
            elif order.created_at < timezone.now() - timedelta(hours=24):
                # Cancel orders that have been pending for more than 24 hours
                order.status = "cancelled"
                order.cancelled_at = timezone.now()
                order.save()

                # Send cancellation email
                send_transactional_email(
                    "order_cancelled",
                    order.customer.id,
                    order_number=order.order_number,
                    order=order,
                )
                processed_count += 1

        logger.info(f"Processed {processed_count} pending orders")
        return processed_count

    except Exception as e:
        logger.error(f"Failed to process pending orders: {str(e)}")
        return 0


@shared_task
def cleanup_old_notifications():
    """
    Clean up old notifications (older than 30 days)
    """
    from apps.notifications.models import Notification

    try:
        # Delete notifications older than 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        old_notifications = Notification.objects.filter(created_at__lt=cutoff_date)
        count = old_notifications.count()
        old_notifications.delete()

        logger.info(f"Cleaned up {count} old notifications")
        return count

    except Exception as e:
        logger.error(f"Failed to cleanup old notifications: {str(e)}")
        return 0
