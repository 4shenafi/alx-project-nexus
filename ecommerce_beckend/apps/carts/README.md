# Carts App - Shopping Cart Management

> **Advanced shopping cart system with real-time validation, persistent sessions, and seamless checkout integration**

## Overview

The Carts app manages shopping cart functionality for NexusCommerce, providing real-time cart management, stock validation, price calculations, and seamless integration with the order processing system. It supports both authenticated and anonymous users with persistent cart sessions.

## Features

### Cart Management
- **Cart Creation**: Automatic cart creation for users and guests
- **Item Management**: Add, update, remove, and clear cart items
- **Real-time Validation**: Stock availability and price validation
- **Persistent Sessions**: Cart persistence across browser sessions
- **Guest Cart Support**: Anonymous user cart functionality
- **Cart Merging**: Automatic cart merging on user login

### Price Calculations
- **Dynamic Pricing**: Real-time price updates and calculations
- **Tax Calculations**: Automatic tax computation based on location
- **Discount Application**: Coupon and promotion code integration
- **Shipping Calculations**: Dynamic shipping cost computation
- **Currency Support**: Multi-currency cart support

### Cart Analytics
- **Abandonment Tracking**: Cart abandonment monitoring
- **Conversion Metrics**: Cart-to-order conversion rates
- **User Behavior**: Cart interaction analytics
- **Performance Monitoring**: Cart operation performance metrics

## Models

### Cart Model
```python
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['user', 'session_key']
```

### CartItem Model
```python
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['cart', 'product_variant']
```

### CartSession Model
```python
class CartSession(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()
```

## API Endpoints

### Cart Management
- `GET /api/v1/carts/` - Get current user's cart
- `POST /api/v1/carts/` - Create new cart
- `DELETE /api/v1/carts/` - Clear current cart
- `GET /api/v1/carts/summary/` - Get cart summary with totals

### Cart Items
- `GET /api/v1/carts/items/` - List cart items
- `POST /api/v1/carts/items/` - Add item to cart
- `PUT /api/v1/carts/items/{id}/` - Update cart item quantity
- `DELETE /api/v1/carts/items/{id}/` - Remove item from cart
- `POST /api/v1/carts/items/bulk-update/` - Bulk update cart items

### Cart Operations
- `POST /api/v1/carts/merge/` - Merge guest cart with user cart
- `POST /api/v1/carts/validate/` - Validate cart items and stock
- `GET /api/v1/carts/checkout-data/` - Get checkout preparation data
- `POST /api/v1/carts/apply-coupon/` - Apply coupon code to cart

## Serializers

### CartSerializer
Cart serialization with items, totals, and metadata.

### CartItemSerializer
Cart item serialization with product information and pricing.

### CartItemCreateSerializer
Specialized serializer for adding items to cart with validation.

### CartSummarySerializer
Optimized serializer for cart summary and checkout preparation.

### CartValidationSerializer
Serializer for cart validation results and error messages.

## Views

### CartViewSet
- Cart retrieval and management
- Cart creation and clearing
- Cart summary generation

### CartItemViewSet
- Cart item CRUD operations
- Quantity updates and validation
- Bulk operations support

### CartOperationsView
- Cart merging functionality
- Cart validation and error handling
- Checkout data preparation

## Cart Management Logic

### Cart Creation
```python
def get_or_create_cart(user=None, session_key=None):
    """Get existing cart or create new one"""
    if user and user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=user,
            defaults={'is_active': True}
        )
    else:
        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            defaults={'is_active': True}
        )
    
    return cart, created
```

### Add Item to Cart
```python
@transaction.atomic
def add_item_to_cart(cart, product_variant, quantity=1):
    """Add item to cart with validation"""
    # Validate stock availability
    if product_variant.stock_quantity < quantity:
        raise InsufficientStockError("Insufficient stock available")
    
    # Get or create cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_variant=product_variant,
        defaults={
            'quantity': quantity,
            'unit_price': product_variant.price,
            'total_price': product_variant.price * quantity
        }
    )
    
    if not created:
        # Update existing item
        cart_item.quantity += quantity
        cart_item.total_price = cart_item.quantity * cart_item.unit_price
        cart_item.save()
    
    return cart_item
```

### Cart Validation
```python
def validate_cart(cart):
    """Validate cart items and return validation results"""
    validation_results = {
        'is_valid': True,
        'errors': [],
        'warnings': [],
        'updated_items': []
    }
    
    for item in cart.items.all():
        # Check stock availability
        if item.product_variant.stock_quantity < item.quantity:
            validation_results['is_valid'] = False
            validation_results['errors'].append({
                'item_id': item.id,
                'message': f"Insufficient stock for {item.product_variant.name}",
                'available_stock': item.product_variant.stock_quantity
            })
        
        # Check price changes
        if item.unit_price != item.product_variant.price:
            validation_results['warnings'].append({
                'item_id': item.id,
                'message': f"Price changed for {item.product_variant.name}",
                'old_price': item.unit_price,
                'new_price': item.product_variant.price
            })
            
            # Update price
            item.unit_price = item.product_variant.price
            item.total_price = item.quantity * item.unit_price
            item.save()
            validation_results['updated_items'].append(item)
    
    return validation_results
```

## Price Calculations

### Cart Totals Calculation
```python
def calculate_cart_totals(cart):
    """Calculate cart totals including taxes and shipping"""
    subtotal = sum(item.total_price for item in cart.items.all())
    
    # Calculate tax (simplified - in real app, use tax service)
    tax_rate = 0.08  # 8% tax rate
    tax_amount = subtotal * tax_rate
    
    # Calculate shipping (simplified - in real app, use shipping service)
    shipping_amount = 0
    if subtotal < 50:  # Free shipping over $50
        shipping_amount = 10.00
    
    total_amount = subtotal + tax_amount + shipping_amount
    
    return {
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'shipping_amount': shipping_amount,
        'total_amount': total_amount,
        'item_count': cart.items.count(),
        'total_quantity': sum(item.quantity for item in cart.items.all())
    }
```

### Dynamic Price Updates
```python
def update_cart_prices(cart):
    """Update cart item prices based on current product prices"""
    updated_items = []
    
    for item in cart.items.all():
        current_price = item.product_variant.price
        if item.unit_price != current_price:
            item.unit_price = current_price
            item.total_price = item.quantity * current_price
            item.save()
            updated_items.append(item)
    
    return updated_items
```

## Session Management

### Guest Cart Persistence
```python
def get_guest_cart(session_key):
    """Get or create guest cart for session"""
    try:
        cart_session = CartSession.objects.get(session_key=session_key)
        if cart_session.expires_at > timezone.now():
            return cart_session.cart
        else:
            cart_session.delete()
    except CartSession.DoesNotExist:
        pass
    
    # Create new cart and session
    cart = Cart.objects.create(session_key=session_key)
    CartSession.objects.create(
        session_key=session_key,
        cart=cart,
        expires_at=timezone.now() + timedelta(days=30)
    )
    
    return cart
```

### Cart Merging
```python
@transaction.atomic
def merge_carts(user_cart, guest_cart):
    """Merge guest cart into user cart"""
    for guest_item in guest_cart.items.all():
        try:
            # Try to find existing item in user cart
            user_item = user_cart.items.get(
                product_variant=guest_item.product_variant
            )
            # Update quantity
            user_item.quantity += guest_item.quantity
            user_item.total_price = user_item.quantity * user_item.unit_price
            user_item.save()
        except CartItem.DoesNotExist:
            # Create new item in user cart
            CartItem.objects.create(
                cart=user_cart,
                product_variant=guest_item.product_variant,
                quantity=guest_item.quantity,
                unit_price=guest_item.unit_price,
                total_price=guest_item.total_price
            )
    
    # Delete guest cart
    guest_cart.delete()
    
    return user_cart
```

## Performance Optimization

### Database Indexing
```python
class Cart(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['session_key', 'is_active']),
            models.Index(fields=['created_at']),
        ]

class CartItem(models.Model):
    # ... fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['cart', 'product_variant']),
            models.Index(fields=['added_at']),
        ]
```

### Caching Strategy
```python
from django.core.cache import cache

def get_cart_summary(cart_id):
    """Get cached cart summary"""
    cache_key = f'cart_summary_{cart_id}'
    summary = cache.get(cache_key)
    
    if summary is None:
        cart = Cart.objects.prefetch_related('items__product_variant').get(id=cart_id)
        summary = calculate_cart_totals(cart)
        cache.set(cache_key, summary, 300)  # Cache for 5 minutes
    
    return summary
```

## Testing

### Test Coverage
- Cart creation and management tests
- Item addition and removal tests
- Price calculation tests
- Session management tests
- Cart merging tests

### Test Commands
```bash
# Run all cart app tests
python manage.py test apps.carts

# Run specific test module
python manage.py test apps.carts.tests.test_models

# Run with coverage
coverage run --source=apps.carts manage.py test apps.carts
```

## Usage Examples

### Add Item to Cart
```python
# Add item to cart
data = {
    'product_variant': 1,
    'quantity': 2
}
response = client.post('/api/v1/carts/items/', data, headers=headers)
cart_item = response.data
```

### Update Cart Item
```python
# Update cart item quantity
data = {
    'quantity': 3
}
response = client.put('/api/v1/carts/items/1/', data, headers=headers)
```

### Get Cart Summary
```python
# Get cart summary
response = client.get('/api/v1/carts/summary/', headers=headers)
summary = response.data
```

### Validate Cart
```python
# Validate cart
response = client.post('/api/v1/carts/validate/', headers=headers)
validation = response.data
```

## Dependencies

- `djangorestframework` - REST API framework
- `django-extensions` - Database utilities
- `celery` - Asynchronous task processing

## Configuration

### Required Settings
```python
# settings.py
CART_SESSION_EXPIRY_DAYS = 30
CART_CACHE_TIMEOUT = 300
FREE_SHIPPING_THRESHOLD = 50.00
DEFAULT_TAX_RATE = 0.08
```

### Environment Variables
```bash
# .env
CART_SESSION_EXPIRY_DAYS=30
FREE_SHIPPING_THRESHOLD=50.00
DEFAULT_TAX_RATE=0.08
```

## Best Practices

### Performance
- Use select_related and prefetch_related for queries
- Implement proper database indexing
- Use caching for frequently accessed data
- Optimize cart calculation queries

### Security
- Validate all cart inputs
- Implement proper session management
- Use CSRF protection
- Sanitize user inputs

### Code Quality
- Follow atomic transaction patterns
- Write comprehensive tests
- Use type hints
- Document all business logic

## Troubleshooting

### Common Issues

1. **Cart Not Persisting**
   - Check session configuration
   - Verify session key handling
   - Check cart expiration settings

2. **Price Calculation Errors**
   - Verify product price updates
   - Check tax calculation logic
   - Review shipping calculation

3. **Stock Validation Issues**
   - Check real-time stock validation
   - Verify inventory updates
   - Review concurrent access handling

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.carts': {
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
