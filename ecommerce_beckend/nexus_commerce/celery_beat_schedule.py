"""
Celery Beat schedule configuration for NexusCommerce
"""

from celery.schedules import crontab

# Celery Beat schedule
CELERY_BEAT_SCHEDULE = {
    # Clean up expired sessions every hour
    "cleanup-expired-sessions": {
        "task": "apps.core.tasks.cleanup_expired_sessions",
        "schedule": crontab(minute=0),  # Every hour
    },
    # Send low stock alerts daily at 9 AM
    "send-low-stock-alerts": {
        "task": "apps.core.tasks.send_low_stock_alerts",
        "schedule": crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    # Update product search index daily at 2 AM
    "update-product-search-index": {
        "task": "apps.core.tasks.update_product_search_index",
        "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    # Generate monthly vendor reports on the 1st of each month at 8 AM
    "generate-monthly-vendor-reports": {
        "task": "apps.core.tasks.generate_monthly_vendor_reports",
        "schedule": crontab(
            day_of_month=1, hour=8, minute=0
        ),  # 1st of each month at 8 AM
    },
    # Process pending orders every 5 minutes
    "process-pending-orders": {
        "task": "apps.core.tasks.process_pending_orders",
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
    # Clean up old notifications weekly on Sunday at 3 AM
    "cleanup-old-notifications": {
        "task": "apps.core.tasks.cleanup_old_notifications",
        "schedule": crontab(day_of_week=0, hour=3, minute=0),  # Sunday at 3 AM
    },
}
