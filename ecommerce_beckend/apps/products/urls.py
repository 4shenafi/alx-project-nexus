"""
Product URLs for NexusCommerce
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "products"

# Create router for viewsets
router = DefaultRouter()
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"brands", views.BrandViewSet, basename="brand")
router.register(r"tags", views.TagViewSet, basename="tag")
router.register(r"", views.ProductViewSet, basename="product")
router.register(r"reviews", views.ProductReviewViewSet, basename="review")

urlpatterns = [
    path("", include(router.urls)),
]
