"""
Cart URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "carts"

# Create router for viewsets
router = DefaultRouter()
router.register(r"", views.CartViewSet, basename="cart")
router.register(r"items", views.CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
]
