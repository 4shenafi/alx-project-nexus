# Orders App - Order Management System

> **Comprehensive order processing, tracking, and management system with atomic transactions and inventory control**

## Overview

The Orders app handles the complete order lifecycle from creation to fulfillment, including order processing, status tracking, inventory management, and order history. It implements atomic transactions to ensure data consistency and provides real-time order tracking capabilities.

## Features

### Order Management
- **Order Creation**: Atomic order creation with inventory validation
- **Order Processing**: Multi-step order processing workflow
- **Status Tracking**: Real-time order status updates
- **Order History**: Complete order history and tracking
- **Order Modifications**: Order updates and cancellations
- **Refund Processing**: Order refund and return management

### Inventory Control
- **Stock Validation**: Real-time stock checking during order creation
- **Inventory Deduction**: Automatic inventory updates on order confirmation
- **Low Stock Alerts**: Automatic notifications for low stock levels
- **Stock Restoration**: Inventory restoration on order cancellation

### Order Analytics
- **Order Statistics**: Order volume and revenue analytics
- **Performance Metrics**: Order processing time and success rates
- **Customer Insights**: Order patterns and customer behavior
- **Vendor Reports**: Order performance by vendor

## Models

### Order Model
```python
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='shipping_orders')
    billing_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='billing_orders')
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### OrderItem Model
```python
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255)  # Static snapshot
    product_sku = models.CharField(max_length=100)   # Static snapshot
    variant_name = models.CharField(max_length=255)  # Static snapshot
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Static snapshot
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
```

### OrderStatusHistory Model
```python
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=20, choices=Order.ORDER_STATUS_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
```

## API Endpoints

### Orders
- `GET /api/v1/orders/` - List user orders
- `GET /api/v1/orders/{id}/` - Get order details
- `POST /api/v1/orders/` - Create new order
- `PUT /api/v1/orders/{id}/` - Update order (Admin/Vendor)
- `PATCH /api/v1/orders/{id}/status/` - Update order status
- `POST /api/v1/orders/{id}/cancel/` - Cancel order
- `GET /api/v1/orders/{id}/tracking/` - Get order tracking info

### Order Items
- `GET /api/v1/orders/{id}/items/` - Get order items
- `POST /api/v1/orders/{id}/items/` - Add item to order (Admin)
- `PUT /api/v1/orders/{id}/items/{item_id}/` - Update order item (Admin)
- `DELETE /api/v1/orders/{id}/items/{item_id}/` - Remove item from order (Admin)

### Order Management (Admin/Vendor)
- `GET /api/v1/orders/admin/` - List all orders (Admin)
- `GET /api/v1/orders/vendor/` - List vendor orders (Vendor)
- `GET /api/v1/orders/analytics/` - Order analytics (Admin)
- `POST /api/v1/orders/bulk-update/` - Bulk order updates (Admin)

## Serializers

### OrderSerializer
Comprehensive order serialization with items, addresses, and status history.

### OrderItemSerializer
Order item serialization with product information and pricing.

### OrderCreateSerializer
Specialized serializer for order creation with validation.

### OrderStatusUpdateSerializer
Serializer for order status updates with validation.

### OrderAnalyticsSerializer
Serializer for order analytics and reporting data.

## Views

### OrderViewSet
- Order listing and detail views
- Order creation with atomic transactions
- Order status management
- Order cancellation handling

### OrderItemViewSet
- Order item management
- Item quantity updates
- Item removal from orders

### OrderAnalyticsView
- Order statistics and metrics
- Revenue analytics
- Performance reporting

### OrderTrackingView
- Real-time order tracking
- Status update notifications
- Delivery tracking integration

## Order Processing Workflow

### 1. Order Creation
```python
@transaction.atomic
def create_order(cart_items, user, shipping_address, billing_address):
    # Validate cart items and stock
    # Create order with pending status
    # Create order items with static pricing
    # Calculate totals and taxes
    # Deduct inventory
    # Send confirmation email
    # Return order object
```

### 2. Order Confirmation
```python
def confirm_order(order_id, payment_data):
    # Validate payment
    # Update order status to confirmed
    # Create status history entry
    # Send confirmation email
    # Trigger inventory updates
    # Notify vendors
```

### 3. Order Processing
```python
def process_order(order_id):
    # Update status to processing
    # Generate shipping labels
    # Update inventory
    # Send processing notification
    # Schedule shipping tasks
```

### 4. Order Fulfillment
```python
def fulfill_order(order_id, tracking_number):
    # Update status to shipped
    # Add tracking information
    # Send shipping notification
    # Update delivery estimates
```

## Atomic Transactions

### Order Creation with Inventory Check
```python
from django.db import transaction

@transaction.atomic
def create_order_with_inventory_check(cart_items, user_data):
    # Lock inventory records
    variants = ProductVariant.objects.select_for_update().filter(
        id__in=[item.variant_id for item in cart_items]
    )
    
    # Validate stock availability
    for item in cart_items:
        variant = variants.get(id=item.variant_id)
        if variant.stock_quantity < item.quantity:
            raise InsufficientStockError(f"Insufficient stock for {variant.name}")
    
    # Create order
    order = Order.objects.create(**order_data)
    
    # Create order items and deduct inventory
    for item in cart_items:
        variant = variants.get(id=item.variant_id)
        OrderItem.objects.create(
            order=order,
            product_variant=variant,
            quantity=item.quantity,
            unit_price=variant.price,
            total_price=variant.price * item.quantity
        )
        variant.stock_quantity -= item.quantity
        variant.save()
    
    return order
```

## Status Management

### Order Status Transitions
```python
ORDER_STATUS_TRANSITIONS = {
    'pending': ['confirmed', 'cancelled'],
    'confirmed': ['processing', 'cancelled'],
    'processing': ['shipped', 'cancelled'],
    'shipped': ['delivered', 'cancelled'],
    'delivered': ['refunded'],
    'cancelled': [],
    'refunded': [],
}

def update_order_status(order, new_status, notes='', user=None):
    if new_status not in ORDER_STATUS_TRANSITIONS.get(order.status, []):
        raise InvalidStatusTransitionError(
            f"Cannot transition from {order.status} to {new_status}"
        )
    
    order.status = new_status
    order.save()
    
    OrderStatusHistory.objects.create(
        order=order,
        status=new_status,
        notes=notes,
        created_by=user
    )
```

## Inventory Management

### Stock Validation
```python
def validate_stock_availability(cart_items):
    """Validate stock availability for all cart items"""
    errors = []
    
    for item in cart_items:
        variant = ProductVariant.objects.get(id=item.variant_id)
        if variant.stock_quantity < item.quantity:
            errors.append({
                'variant_id': variant.id,
                'variant_name': variant.name,
                'requested': item.quantity,
                'available': variant.stock_quantity
            })
    
    if errors:
        raise InsufficientStockError(errors)
    
    return True
```

### Inventory Deduction
```python
@transaction.atomic
def deduct_inventory(order_items):
    """Deduct inventory for order items"""
    for item in order_items:
        variant = ProductVariant.objects.select_for_update().get(
            id=item.product_variant_id
        )
        variant.stock_quantity -= item.quantity
        variant.save()
        
        # Check for low stock alerts
        if variant.stock_quantity <= variant.low_stock_threshold:
            send_low_stock_alert.delay(variant.id)
```

## Testing

### Test Coverage
- Order creation and validation tests
- Inventory management tests
- Status transition tests
- Atomic transaction tests
- Order analytics tests

### Test Commands
```bash
# Run all order app tests
python manage.py test apps.orders

# Run specific test module
python manage.py test apps.orders.tests.test_models

# Run with coverage
coverage run --source=apps.orders manage.py test apps.orders
```

## Usage Examples

### Create Order
```python
# Create new order
data = {
    'shipping_address': 1,
    'billing_address': 1,
    'payment_method': 'credit_card',
    'notes': 'Please deliver during business hours'
}
response = client.post('/api/v1/orders/', data, headers=headers)
order = response.data
```

### Update Order Status
```python
# Update order status
data = {
    'status': 'shipped',
    'notes': 'Order shipped via FedEx',
    'tracking_number': '1234567890'
}
response = client.patch('/api/v1/orders/1/status/', data, headers=headers)
```

### Get Order Analytics
```python
# Get order analytics
response = client.get('/api/v1/orders/analytics/?period=month', headers=headers)
analytics = response.data
```

## Dependencies

- `djangorestframework` - REST API framework
- `django-extensions` - Database utilities
- `celery` - Asynchronous task processing
- `django-ratelimit` - Rate limiting

## Configuration

### Required Settings
```python
# settings.py
ORDER_NUMBER_PREFIX = 'ORD'
ORDER_NUMBER_LENGTH = 8
DEFAULT_ORDER_STATUS = 'pending'
AUTO_CONFIRM_ORDERS = False
```

### Environment Variables
```bash
# .env
ORDER_NUMBER_PREFIX=ORD
AUTO_CONFIRM_ORDERS=False
LOW_STOCK_THRESHOLD=5
```

## Best Practices

### Performance
- Use select_related and prefetch_related for queries
- Implement proper database indexing
- Use atomic transactions for data consistency
- Cache frequently accessed order data

### Security
- Validate all order inputs
- Implement proper permission checks
- Use CSRF protection
- Log all order modifications

### Code Quality
- Follow atomic transaction patterns
- Write comprehensive tests
- Use type hints
- Document all business logic

## Troubleshooting

### Common Issues

1. **Inventory Inconsistency**
   - Check for concurrent order processing
   - Verify atomic transaction usage
   - Review inventory deduction logic

2. **Order Status Issues**
   - Verify status transition rules
   - Check permission requirements
   - Review status history logging

3. **Performance Issues**
   - Check database query optimization
   - Verify indexing strategy
   - Monitor transaction locks

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.orders': {
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
