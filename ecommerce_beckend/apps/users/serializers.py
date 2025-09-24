"""
User serializers for NexusCommerce
"""

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import User, UserAddress, UserProfile


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "date_of_birth",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "username": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Create user profile
        UserProfile.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """

    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            attrs["user"] = user
        else:
            raise serializers.ValidationError("Must include email and password.")

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile
    """

    full_name = serializers.ReadOnlyField()
    is_vendor = serializers.ReadOnlyField()
    is_admin = serializers.ReadOnlyField()
    is_approved_vendor = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "date_of_birth",
            "role",
            "status",
            "is_email_verified",
            "is_vendor",
            "is_admin",
            "is_approved_vendor",
            "date_joined",
            "last_login",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "status",
            "is_email_verified",
            "date_joined",
            "last_login",
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """

    class Meta:
        model = UserProfile
        fields = [
            "bio",
            "avatar",
            "website",
            "location",
            "preferences",
        ]


class UserAddressSerializer(serializers.ModelSerializer):
    """
    Serializer for user addresses
    """

    class Meta:
        model = UserAddress
        fields = [
            "id",
            "address_type",
            "is_default",
            "first_name",
            "last_name",
            "company",
            "address_line_1",
            "address_line_2",
            "city",
            "state_province",
            "postal_code",
            "country",
            "phone_number",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        # Ensure only one default address per type per user
        if attrs.get("is_default", False):
            user = self.context["request"].user
            address_type = attrs.get("address_type")

            # Exclude current instance if updating
            queryset = UserAddress.objects.filter(
                user=user, address_type=address_type, is_default=True
            )
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    f"You already have a default {address_type} address."
                )

        return attrs


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for email verification
    """

    token = serializers.CharField()

    def validate_token(self, value):
        try:
            user = User.objects.get(email_verification_token=value)
            if user.is_email_verified:
                raise serializers.ValidationError("Email is already verified.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")
        return value


class PasswordResetRequestSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """

    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for password reset confirmation
    """

    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def validate_token(self, value):
        try:
            user = User.objects.get(email_verification_token=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid reset token.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing password
    """

    current_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    new_password_confirm = serializers.CharField()

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
