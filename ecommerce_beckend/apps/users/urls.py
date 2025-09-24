"""
User URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "users"

# Create router for viewsets
router = DefaultRouter()
router.register(r"profiles", views.UserProfileViewSet, basename="profile")
router.register(r"addresses", views.UserAddressViewSet, basename="address")

urlpatterns = [
    # Authentication endpoints
    path("register/", views.UserRegistrationView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Email verification
    path(
        "verify-email/",
        views.EmailVerificationView.as_view(),
        name="verify_email",
    ),
    path("resend-otp/", views.ResendOTPView.as_view(), name="resend_otp"),
    # Password management
    path(
        "password-reset/",
        views.PasswordResetRequestView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
    # Include router URLs
    path("", include(router.urls)),
]
