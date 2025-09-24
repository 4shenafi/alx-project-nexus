"""
Standardized API schemas for NexusCommerce
"""

from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    """
    Standardized error response schema for all API endpoints.

    This schema ensures consistent error responses across the entire API,
    making it easier for API consumers to handle errors programmatically.
    """

    status = serializers.CharField(
        help_text="Response status indicator, always 'error' for error responses"
    )
    error = serializers.DictField(
        child=serializers.CharField(),
        help_text="Error details containing code, message, and optional details",
    )


class SuccessResponseSerializer(serializers.Serializer):
    """
    Standardized success response schema for all API endpoints.
    """

    status = serializers.CharField(
        help_text="Response status indicator, always 'success' for successful responses"
    )
    data = serializers.DictField(
        help_text="Response data containing the actual payload"
    )


class PaginatedResponseSerializer(serializers.Serializer):
    """
    Standardized paginated response schema for list endpoints.
    """

    count = serializers.IntegerField(help_text="Total number of items across all pages")
    next = serializers.URLField(
        allow_null=True,
        help_text="URL to the next page of results, null if this is the last page",
    )
    previous = serializers.URLField(
        allow_null=True,
        help_text="URL to the previous page of results, null if this is the first page",
    )
    results = serializers.ListField(help_text="List of items for the current page")
