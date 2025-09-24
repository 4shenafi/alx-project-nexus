"""
Payment URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "payments"

# Create router for viewsets
router = DefaultRouter()
router.register(r"methods", views.PaymentMethodViewSet, basename="payment-method")
router.register(r"", views.PaymentViewSet, basename="payment")
router.register(r"refunds", views.RefundViewSet, basename="refund")

urlpatterns = [
    path("", include(router.urls)),
]
