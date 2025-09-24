"""
Product views for NexusCommerce
"""

from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import (IsOwnerOrAdmin, IsVendorOrAdmin,
                                    IsVendorOwnerOrAdmin,
                                    ReadOnlyOrAuthenticated)

from .models import (Brand, Category, Product, ProductReview, ProductVariant,
                     Tag)
from .serializers import (BrandSerializer, CategorySerializer,
                          ProductCreateUpdateSerializer,
                          ProductDetailSerializer, ProductListSerializer,
                          ProductReviewCreateSerializer,
                          ProductReviewSerializer, TagSerializer)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Category viewset for listing and retrieving categories
    """

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @extend_schema(
        summary="List categories",
        description="Get all active categories with hierarchical structure",
        responses={200: {"description": "Categories retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get category details",
        description="Get detailed information about a specific category",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Brand viewset for listing and retrieving brands
    """

    queryset = Brand.objects.filter(is_active=True)
    serializer_class = BrandSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @extend_schema(
        summary="List brands",
        description="Get all active brands",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Tag viewset for listing and retrieving tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = "slug"

    @extend_schema(
        summary="List tags",
        description="Get all available tags",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product viewset with full CRUD operations
    """

    queryset = Product.objects.select_related(
        "vendor", "category", "brand"
    ).prefetch_related("tags", "variants", "images", "reviews")
    permission_classes = [ReadOnlyOrAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = [
        "category",
        "brand",
        "tags",
        "status",
        "is_featured",
        "is_digital",
    ]
    search_fields = ["name", "description", "short_description", "sku"]
    ordering_fields = ["name", "created_at", "updated_at", "price"]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsVendorOrAdmin]
        elif self.action in ["my_products"]:
            self.permission_classes = [IsVendorOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by vendor for vendor users
        if self.request.user.is_authenticated and self.request.user.is_vendor:
            if self.action == "my_products":
                return queryset.filter(vendor=self.request.user)
            elif not self.request.user.is_admin:
                # Vendors can only see their own products in detail view
                if self.action == "retrieve":
                    return queryset.filter(vendor=self.request.user)

        # Public users can only see active products
        if not self.request.user.is_authenticated or not self.request.user.is_admin:
            queryset = queryset.filter(status="active")

        return queryset

    @extend_schema(
        summary="List products",
        description="Get all products with filtering, searching, and sorting",
        parameters=[
            OpenApiParameter(
                name="category",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by category slug",
            ),
            OpenApiParameter(
                name="brand",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by brand slug",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search in product name and description",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Order by field (e.g., 'name', '-created_at')",
            ),
        ],
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Apply price filtering
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price:
            queryset = queryset.filter(variants__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(variants__price__lte=max_price)

        # Apply stock filtering
        in_stock = request.query_params.get("in_stock")
        if in_stock and in_stock.lower() == "true":
            queryset = queryset.filter(variants__stock_quantity__gt=0)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get product details",
        description="Get detailed information about a specific product",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create product",
        description="Create a new product with variants and images",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Set vendor to current user
        product = serializer.save(vendor=request.user)

        return Response(
            {
                "status": "success",
                "data": ProductDetailSerializer(product).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Update product",
        description="Update an existing product",
        responses={200: {"description": "Item retrieved successfully"}},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(
            {
                "status": "success",
                "data": ProductDetailSerializer(product).data,
            }
        )

    @extend_schema(
        summary="Get vendor products",
        description="Get all products for the current vendor",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def my_products(self, request):
        queryset = self.get_queryset().filter(vendor=request.user)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Get featured products",
        description="Get all featured products",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(detail=False, methods=["get"])
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True, status="active")
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )


class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    Product review viewset
    """

    queryset = ProductReview.objects.select_related("user", "product")
    permission_classes = [ReadOnlyOrAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = [
        "product",
        "rating",
        "is_verified_purchase",
        "is_approved",
    ]
    ordering_fields = ["created_at", "rating", "helpful_count"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "create":
            return ProductReviewCreateSerializer
        return ProductReviewSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwnerOrAdmin]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()

        # Only show approved reviews to public
        if not self.request.user.is_authenticated or not self.request.user.is_admin:
            queryset = queryset.filter(is_approved=True)

        return queryset

    @extend_schema(
        summary="List product reviews",
        description="Get all reviews for products",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )

    @extend_schema(
        summary="Create product review",
        description="Create a new review for a product",
        responses={201: {"description": "Item created successfully"}},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save()

        return Response(
            {
                "status": "success",
                "data": ProductReviewSerializer(review).data,
            },
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Get product reviews",
        description="Get all reviews for a specific product",
        responses={200: {"description": "Items retrieved successfully"}},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="product/(?P<product_slug>[^/.]+)",
    )
    def product_reviews(self, request, product_slug=None):
        product = get_object_or_404(Product, slug=product_slug)
        queryset = self.get_queryset().filter(product=product)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "data": serializer.data,
            }
        )
