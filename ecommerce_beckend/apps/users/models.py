"""
User models for NexusCommerce
"""

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model extending AbstractUser
    Uses email as the primary identifier
    """

    ROLE_CHOICES = [
        ("customer", "Customer"),
        ("vendor", "Vendor"),
        ("admin", "Admin"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("suspended", "Suspended"),
        ("pending_approval", "Pending Approval"),
    ]

    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        help_text="Required. Must be a valid email address.",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer",
        db_index=True,
        help_text="User role determining permissions",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="active",
        db_index=True,
        help_text="Account status",
    )
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True,
        help_text="Optional phone number",
    )
    date_of_birth = models.DateField(
        blank=True, null=True, help_text="Optional date of birth"
    )
    is_email_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether the email address has been verified",
    )
    email_verification_token = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Token for email verification",
    )
    email_verification_otp = models.CharField(
        max_length=6,
        blank=True,
        null=True,
        help_text="OTP for email verification",
    )
    email_verification_otp_expires_at = models.DateTimeField(
        blank=True, null=True, help_text="OTP expiration time"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Override username to use email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["role"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_email_verified"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_vendor(self):
        """Check if user is a vendor"""
        return self.role == "vendor"

    @property
    def is_admin(self):
        """Check if user is an admin"""
        return self.role == "admin"

    @property
    def is_approved_vendor(self):
        """Check if user is an approved vendor"""
        return self.role == "vendor" and self.status == "active"


class UserAddress(models.Model):
    """
    User address model for shipping and billing addresses
    """

    ADDRESS_TYPE_CHOICES = [
        ("shipping", "Shipping"),
        ("billing", "Billing"),
        ("both", "Both"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="addresses", db_index=True
    )
    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE_CHOICES,
        default="both",
        db_index=True,
    )
    is_default = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether this is the default address for this type",
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=100, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_addresses"
        verbose_name = "User Address"
        verbose_name_plural = "User Addresses"
        indexes = [
            models.Index(fields=["user", "address_type"]),
            models.Index(fields=["user", "is_default"]),
        ]
        unique_together = [
            ["user", "address_type", "is_default"],
        ]

    def __str__(self):
        return f"{self.user.email} - {self.get_address_type_display()} Address"

    def save(self, *args, **kwargs):
        # Ensure only one default address per type per user
        if self.is_default:
            UserAddress.objects.filter(
                user=self.user, address_type=self.address_type, is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    Extended user profile information
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", db_index=True
    )
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        help_text="User profile picture",
    )
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    preferences = models.JSONField(
        default=dict, blank=True, help_text="User preferences and settings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_profiles"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.email} Profile"
