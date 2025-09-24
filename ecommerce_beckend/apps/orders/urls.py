"""
Order URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "orders"

# Create router for viewsets
router = DefaultRouter()
router.register(
    r"shipping-methods",
    views.ShippingMethodViewSet,
    basename="shipping-method",
)
router.register(r"", views.OrderViewSet, basename="order")
router.register(
    r"(?P<order_pk>[^/.]+)/history",
    views.OrderStatusHistoryViewSet,
    basename="order-history",
)

urlpatterns = [
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("", include(router.urls)),
]
