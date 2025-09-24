# Products App - Product Catalog Management

> **Comprehensive product catalog system with categories, variants, attributes, reviews, and advanced search capabilities**

## Overview

The Products app manages the entire product catalog for NexusCommerce, including product information, categories, variants, attributes, images, reviews, and search functionality. It provides a flexible and scalable system for managing complex product hierarchies and relationships.

## Features

### Product Management
- **Product Catalog**: Complete product information management
- **Product Variants**: Size, color, material, and custom attribute variants
- **Product Categories**: Hierarchical category system with unlimited nesting
- **Product Attributes**: Custom attributes and specifications
- **Product Images**: Multiple images with thumbnail generation
- **Product Reviews**: Customer reviews and ratings system
- **Inventory Management**: Stock tracking and low stock alerts

### Search & Filtering
- **Full-Text Search**: Advanced search across product names and descriptions
- **Category Filtering**: Filter products by categories and subcategories
- **Attribute Filtering**: Filter by product attributes and variants
- **Price Range Filtering**: Filter products by price range
- **Brand Filtering**: Filter products by brand
- **Sorting Options**: Sort by price, popularity, rating, date added

### Vendor Management
- **Vendor Products**: Products associated with specific vendors
- **Vendor Approval**: Admin approval for vendor products
- **Vendor Analytics**: Product performance metrics for vendors

## Models

### Category Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Product Model
```python
class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ProductVariant Model
```python
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### ProductAttribute Model
```python
class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0)
```

### ProductImage Model
```python
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
```

### ProductReview Model
```python
class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=255)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## API Endpoints

### Categories
- `GET /api/v1/products/categories/` - List all categories
- `GET /api/v1/products/categories/{id}/` - Get category details
- `GET /api/v1/products/categories/{id}/products/` - Get products in category
- `POST /api/v1/products/categories/` - Create category (Admin/Vendor)
- `PUT /api/v1/products/categories/{id}/` - Update category (Admin/Vendor)
- `DELETE /api/v1/products/categories/{id}/` - Delete category (Admin)

### Products
- `GET /api/v1/products/` - List products with filtering and search
- `GET /api/v1/products/{id}/` - Get product details
- `GET /api/v1/products/{id}/variants/` - Get product variants
- `GET /api/v1/products/{id}/reviews/` - Get product reviews
- `POST /api/v1/products/` - Create product (Vendor)
- `PUT /api/v1/products/{id}/` - Update product (Owner/Admin)
- `DELETE /api/v1/products/{id}/` - Delete product (Owner/Admin)

### Product Variants
- `GET /api/v1/products/variants/` - List variants
- `GET /api/v1/products/variants/{id}/` - Get variant details
- `POST /api/v1/products/variants/` - Create variant (Vendor)
- `PUT /api/v1/products/variants/{id}/` - Update variant (Owner/Admin)
- `DELETE /api/v1/products/variants/{id}/` - Delete variant (Owner/Admin)

### Product Reviews
- `GET /api/v1/products/reviews/` - List reviews
- `POST /api/v1/products/reviews/` - Create review (Authenticated)
- `PUT /api/v1/products/reviews/{id}/` - Update review (Owner)
- `DELETE /api/v1/products/reviews/{id}/` - Delete review (Owner/Admin)

### Search & Filtering
- `GET /api/v1/products/search/?q={query}` - Search products
- `GET /api/v1/products/?category={id}` - Filter by category
- `GET /api/v1/products/?brand={id}` - Filter by brand
- `GET /api/v1/products/?min_price={price}&max_price={price}` - Filter by price
- `GET /api/v1/products/?sort={field}` - Sort products

## Serializers

### CategorySerializer
Handles category serialization with nested children and product counts.

### ProductSerializer
Comprehensive product serialization including variants, images, and reviews.

### ProductVariantSerializer
Variant serialization with stock information and pricing.

### ProductReviewSerializer
Review serialization with user information and approval status.

### ProductSearchSerializer
Optimized serializer for search results with highlighting.

## Views

### CategoryViewSet
- CRUD operations for categories
- Hierarchical category listing
- Category product filtering

### ProductViewSet
- Product listing with advanced filtering
- Product detail with related data
- Product creation and management

### ProductVariantViewSet
- Variant management
- Stock tracking
- Price management

### ProductReviewViewSet
- Review creation and management
- Review approval workflow
- Rating aggregation

### ProductSearchView
- Full-text search implementation
- Search result optimization
- Search analytics

## Search Implementation

### Full-Text Search
```python
# Using PostgreSQL full-text search
from django.contrib.postgres.search import SearchVector, SearchQuery

def search_products(query):
    search_vector = SearchVector('name', 'description', 'short_description')
    search_query = SearchQuery(query)
    return Product.objects.annotate(
        search=search_vector
    ).filter(search=search_query).order_by('-search_rank')
```

### Filtering System
```python
class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    min_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='variants__price', lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(field_name='variants__stock_quantity', lookup_expr='gt')
```

## Image Management

### Image Processing
- Automatic thumbnail generation
- Multiple image sizes
- WebP format support
- Image optimization

### Storage Configuration
```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'nexuscommerce-media'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
```

## Performance Optimization

### Database Indexing
```python
class Product(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
            models.Index(fields=['vendor', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_featured']),
        ]
```

### Caching Strategy
```python
# Cache frequently accessed data
@cache_page(60 * 15)  # 15 minutes
def category_list(request):
    return Category.objects.filter(is_active=True)

# Cache product details
@cache_page(60 * 30)  # 30 minutes
def product_detail(request, pk):
    return Product.objects.select_related('category', 'brand').prefetch_related('variants', 'images').get(pk=pk)
```

## Testing

### Test Coverage
- Model validation tests
- API endpoint tests
- Search functionality tests
- Image upload tests
- Review system tests

### Test Commands
```bash
# Run all product app tests
python manage.py test apps.products

# Run specific test module
python manage.py test apps.products.tests.test_models

# Run with coverage
coverage run --source=apps.products manage.py test apps.products
```

## Usage Examples

### Create Product
```python
# Create new product
data = {
    'name': 'Premium Wireless Headphones',
    'description': 'High-quality wireless headphones with noise cancellation',
    'category': 1,
    'brand': 1,
    'variants': [
        {
            'sku': 'PWH-001',
            'name': 'Black',
            'price': '199.99',
            'stock_quantity': 50
        }
    ]
}
response = client.post('/api/v1/products/', data, headers=headers)
```

### Search Products
```python
# Search products
response = client.get('/api/v1/products/search/?q=wireless headphones')
products = response.data['results']
```

### Filter Products
```python
# Filter by category and price
response = client.get('/api/v1/products/?category=1&min_price=100&max_price=300')
products = response.data['results']
```

## Dependencies

- `djangorestframework` - REST API framework
- `django-filter` - Advanced filtering
- `Pillow` - Image processing
- `django-storages` - Cloud storage support
- `celery` - Asynchronous image processing

## Configuration

### Required Settings
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
```

### Environment Variables
```bash
# .env
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

## Best Practices

### Performance
- Use select_related and prefetch_related for queries
- Implement proper database indexing
- Use caching for frequently accessed data
- Optimize image sizes and formats

### Security
- Validate all user inputs
- Implement proper file upload security
- Use CSRF protection
- Sanitize search queries

### Code Quality
- Follow DRY principles
- Write comprehensive tests
- Use type hints
- Document all public methods

## Troubleshooting

### Common Issues

1. **Search Not Working**
   - Check PostgreSQL full-text search configuration
   - Verify search indexes are created
   - Check search query syntax

2. **Image Upload Issues**
   - Verify file permissions
   - Check storage configuration
   - Ensure proper image formats

3. **Performance Issues**
   - Check database query optimization
   - Verify caching configuration
   - Monitor database indexes

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.products': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}
```

## Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Ensure all tests pass
5. Submit pull request with clear description

## License

This app is part of the NexusCommerce project and follows the same licensing terms.
