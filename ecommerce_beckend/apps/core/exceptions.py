"""
Custom exception handlers for NexusCommerce API
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error response format
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            "status": "error",
            "error": {
                "code": get_error_code(exc),
                "message": get_error_message(exc),
                "details": get_error_details(exc, response),
            },
        }
        response.data = custom_response_data

    return response


def get_error_code(exc):
    """Get machine-readable error code"""
    if hasattr(exc, "default_code"):
        return exc.default_code
    elif hasattr(exc, "code"):
        return exc.code
    else:
        return exc.__class__.__name__.lower()


def get_error_message(exc):
    """Get human-readable error message"""
    if hasattr(exc, "detail"):
        if isinstance(exc.detail, dict):
            return "Validation failed"
        elif isinstance(exc.detail, list):
            return exc.detail[0] if exc.detail else "An error occurred"
        else:
            return str(exc.detail)
    elif hasattr(exc, "message"):
        return exc.message
    else:
        return str(exc)


def get_error_details(exc, response):
    """Get detailed error information"""
    if hasattr(exc, "detail") and isinstance(exc.detail, dict):
        return exc.detail
    elif isinstance(exc, ValidationError):
        return (
            exc.message_dict
            if hasattr(exc, "message_dict")
            else {"non_field_errors": [str(exc)]}
        )
    elif isinstance(exc, IntegrityError):
        return {"database": ["Database integrity constraint violation"]}
    else:
        return None
