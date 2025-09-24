"""
Admin configuration for users app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User, UserAddress, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User admin
    """

    list_display = [
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "status",
        "is_email_verified",
        "is_active",
        "date_joined",
    ]
    list_filter = [
        "role",
        "status",
        "is_email_verified",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    ]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-date_joined"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "date_of_birth",
                )
            },
        ),
        (
            "Account info",
            {
                "fields": (
                    "role",
                    "status",
                    "is_email_verified",
                    "email_verification_token",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """
    UserAddress admin
    """

    list_display = [
        "user",
        "address_type",
        "is_default",
        "first_name",
        "last_name",
        "city",
        "country",
        "created_at",
    ]
    list_filter = ["address_type", "is_default", "country", "created_at"]
    search_fields = [
        "user__email",
        "first_name",
        "last_name",
        "city",
        "country",
    ]
    ordering = ["-created_at"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    UserProfile admin
    """

    list_display = [
        "user",
        "location",
        "website",
        "created_at",
    ]
    list_filter = ["created_at"]
    search_fields = ["user__email", "location", "website"]
    ordering = ["-created_at"]
