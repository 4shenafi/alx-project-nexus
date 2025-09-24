"""
Core views for NexusCommerce
"""

import psycopg2
import redis
from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


def health_check(request):
    """
    Health check endpoint for monitoring
    """
    health_status = {
        "status": "healthy",
        "checks": {
            "database": False,
            "cache": False,
            "celery": False,
        },
        "version": "1.0.0",
    }

    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status["checks"]["database"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = False
        health_status["database_error"] = str(e)

    # Check cache connection
    try:
        cache.set("health_check", "ok", 10)
        if cache.get("health_check") == "ok":
            health_status["checks"]["cache"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["cache"] = False
        health_status["cache_error"] = str(e)

    # Check Redis connection
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        health_status["checks"]["celery"] = True
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["celery"] = False
        health_status["celery_error"] = str(e)

    # Determine overall status
    if not all(health_status["checks"].values()):
        health_status["status"] = "unhealthy"

    status_code = 200 if health_status["status"] == "healthy" else 503
    return JsonResponse(health_status, status=status_code)
