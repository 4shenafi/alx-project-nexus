# Core App - Foundation & Utilities

> **Core utilities, shared components, and foundational functionality for the NexusCommerce platform**

## Overview

The Core app provides essential utilities, shared components, and foundational functionality that supports the entire NexusCommerce platform. It includes custom exceptions, base classes, utility functions, and core business logic that other apps depend on.

## Features

### Exception Handling
- **Custom Exceptions**: Standardized exception classes for consistent error handling
- **Error Responses**: Standardized error response formats
- **Exception Middleware**: Global exception handling middleware
- **Error Logging**: Comprehensive error logging and monitoring

### Utility Functions
- **Common Utilities**: Shared utility functions across the platform
- **Data Validation**: Common validation functions and helpers
- **Formatting Utilities**: Data formatting and transformation functions
- **Date/Time Utilities**: Date and time manipulation helpers

### Base Classes
- **Base Models**: Abstract base model classes with common functionality
- **Base Views**: Base view classes with common patterns
- **Base Serializers**: Base serializer classes with shared functionality
- **Base Permissions**: Common permission classes

### Health Monitoring
- **Health Checks**: System health monitoring endpoints
- **Status Monitoring**: Application status and dependency checks
- **Performance Metrics**: Basic performance monitoring
- **System Information**: System information and diagnostics

## Models

### Base Model
```python
class BaseModel(models.Model):
    """Abstract base model with common fields and functionality"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        """Soft delete the instance"""
        self.is_active = False
        self.save()
    
    def restore(self):
        """Restore a soft-deleted instance"""
        self.is_active = True
        self.save()
```

### Audit Model
```python
class AuditModel(BaseModel):
    """Abstract model with audit trail functionality"""
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='%(class)s_updated'
    )
    
    class Meta:
        abstract = True
```

## API Endpoints

### Health & Status
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/detailed/` - Detailed health check with dependencies
- `GET /api/v1/status/` - Application status information
- `GET /api/v1/version/` - Application version information

### System Information
- `GET /api/v1/system/info/` - System information
- `GET /api/v1/system/metrics/` - Basic system metrics
- `GET /api/v1/system/config/` - Public configuration information

## Serializers

### HealthCheckSerializer
```python
class HealthCheckSerializer(serializers.Serializer):
    status = serializers.CharField()
    timestamp = serializers.DateTimeField()
    version = serializers.CharField()
    uptime = serializers.DurationField()
    dependencies = serializers.DictField()
```

### ErrorResponseSerializer
```python
class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
    message = serializers.CharField()
    details = serializers.DictField(required=False)
    timestamp = serializers.DateTimeField()
    request_id = serializers.CharField(required=False)
```

## Views

### HealthCheckView
```python
class HealthCheckView(APIView):
    """Basic health check endpoint"""
    
    def get(self, request):
        """Return basic health status"""
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now(),
            'version': settings.VERSION,
            'uptime': get_uptime()
        })
```

### DetailedHealthCheckView
```python
class DetailedHealthCheckView(APIView):
    """Detailed health check with dependency status"""
    
    def get(self, request):
        """Return detailed health status with dependencies"""
        dependencies = {
            'database': check_database_health(),
            'redis': check_redis_health(),
            'celery': check_celery_health(),
            'external_apis': check_external_apis_health()
        }
        
        overall_status = 'healthy' if all(dependencies.values()) else 'unhealthy'
        
        return Response({
            'status': overall_status,
            'timestamp': timezone.now(),
            'version': settings.VERSION,
            'uptime': get_uptime(),
            'dependencies': dependencies
        })
```

## Exception Handling

### Custom Exceptions
```python
class NexusCommerceException(Exception):
    """Base exception for NexusCommerce"""
    pass

class ValidationError(NexusCommerceException):
    """Custom validation error"""
    pass

class BusinessLogicError(NexusCommerceException):
    """Business logic error"""
    pass

class ExternalServiceError(NexusCommerceException):
    """External service error"""
    pass

class InsufficientStockError(BusinessLogicError):
    """Insufficient stock error"""
    pass

class PaymentProcessingError(BusinessLogicError):
    """Payment processing error"""
    pass

class NotificationError(BusinessLogicError):
    """Notification error"""
    pass
```

### Exception Handler
```python
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """Custom exception handler for DRF"""
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': 'API Error',
            'message': str(exc),
            'timestamp': timezone.now().isoformat(),
            'request_id': context.get('request_id', ''),
            'details': response.data if isinstance(response.data, dict) else {}
        }
        
        # Log the error
        logger.error(f"API Error: {exc}", extra={
            'request_id': context.get('request_id', ''),
            'user': context.get('request').user.id if context.get('request').user.is_authenticated else None,
            'path': context.get('request').path,
            'method': context.get('request').method
        })
        
        response.data = custom_response_data
    
    return response
```

## Utility Functions

### Data Validation
```python
def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    import re
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

def validate_currency(currency):
    """Validate currency code"""
    valid_currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD']
    return currency.upper() in valid_currencies
```

### Data Formatting
```python
def format_currency(amount, currency='USD'):
    """Format amount as currency"""
    return f"{currency} {amount:,.2f}"

def format_phone(phone):
    """Format phone number"""
    import re
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 10:
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    return phone

def format_date(date, format='%Y-%m-%d'):
    """Format date"""
    if date:
        return date.strftime(format)
    return None
```

### Date/Time Utilities
```python
from datetime import datetime, timedelta
from django.utils import timezone

def get_uptime():
    """Get application uptime"""
    # This would typically be stored at application startup
    start_time = getattr(settings, 'APP_START_TIME', timezone.now())
    return timezone.now() - start_time

def is_business_hours(dt=None):
    """Check if datetime is within business hours"""
    if dt is None:
        dt = timezone.now()
    
    # Monday to Friday, 9 AM to 5 PM
    return dt.weekday() < 5 and 9 <= dt.hour < 17

def get_next_business_day(dt=None):
    """Get next business day"""
    if dt is None:
        dt = timezone.now()
    
    next_day = dt + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip weekends
        next_day += timedelta(days=1)
    
    return next_day.replace(hour=9, minute=0, second=0, microsecond=0)
```

## Health Check Functions

### Database Health Check
```python
def check_database_health():
    """Check database connectivity and performance"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            return result[0] == 1
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
```

### Redis Health Check
```python
def check_redis_health():
    """Check Redis connectivity"""
    try:
        from django.core.cache import cache
        cache.set('health_check', 'ok', 10)
        result = cache.get('health_check')
        return result == 'ok'
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False
```

### Celery Health Check
```python
def check_celery_health():
    """Check Celery worker availability"""
    try:
        from celery import current_app
        inspect = current_app.control.inspect()
        stats = inspect.stats()
        return bool(stats)
    except Exception as e:
        logger.error(f"Celery health check failed: {e}")
        return False
```

### External APIs Health Check
```python
def check_external_apis_health():
    """Check external API availability"""
    try:
        import requests
        
        # Check payment provider
        payment_status = check_payment_provider_health()
        
        # Check email service
        email_status = check_email_service_health()
        
        # Check SMS service
        sms_status = check_sms_service_health()
        
        return {
            'payment_provider': payment_status,
            'email_service': email_status,
            'sms_service': sms_status
        }
    except Exception as e:
        logger.error(f"External APIs health check failed: {e}")
        return False

def check_payment_provider_health():
    """Check payment provider health"""
    try:
        # This would be a simple ping to your payment provider
        # For example, with Stripe:
        # stripe.Account.retrieve()
        return True
    except Exception:
        return False

def check_email_service_health():
    """Check email service health"""
    try:
        from django.core.mail import get_connection
        connection = get_connection()
        connection.open()
        connection.close()
        return True
    except Exception:
        return False

def check_sms_service_health():
    """Check SMS service health"""
    try:
        # This would check your SMS provider
        # For example, with Twilio:
        # client.api.accounts.get(settings.TWILIO_ACCOUNT_SID)
        return True
    except Exception:
        return False
```

## Base Classes

### Base ViewSet
```python
class BaseViewSet(viewsets.ModelViewSet):
    """Base ViewSet with common functionality"""
    
    def get_queryset(self):
        """Filter queryset by user if applicable"""
        queryset = super().get_queryset()
        
        # Filter by user if model has user field
        if hasattr(self.queryset.model, 'user'):
            if self.request.user.is_authenticated:
                queryset = queryset.filter(user=self.request.user)
            else:
                queryset = queryset.none()
        
        return queryset
    
    def perform_create(self, serializer):
        """Set user on creation if applicable"""
        if hasattr(serializer.Meta.model, 'user'):
            serializer.save(user=self.request.user)
        else:
            serializer.save()
```

### Base Permission
```python
class BasePermission(permissions.BasePermission):
    """Base permission class with common functionality"""
    
    def has_permission(self, request, view):
        """Check if user has permission"""
        if not request.user.is_authenticated:
            return False
        
        return self.check_permission(request, view)
    
    def check_permission(self, request, view):
        """Override this method in subclasses"""
        return True
```

## Testing

### Test Coverage
- Utility function tests
- Exception handling tests
- Health check tests
- Base class functionality tests

### Test Commands
```bash
# Run all core app tests
python manage.py test apps.core

# Run specific test module
python manage.py test apps.core.tests.test_utils

# Run with coverage
coverage run --source=apps.core manage.py test apps.core
```

## Usage Examples

### Health Check
```python
# Basic health check
response = client.get('/api/v1/health/')
health_data = response.data

# Detailed health check
response = client.get('/api/v1/health/detailed/')
detailed_health = response.data
```

### Using Utility Functions
```python
from apps.core.utils import validate_email, format_currency

# Validate email
is_valid = validate_email('user@example.com')

# Format currency
formatted = format_currency(99.99, 'USD')
```

### Using Base Classes
```python
from apps.core.views import BaseViewSet
from apps.core.permissions import BasePermission

class MyViewSet(BaseViewSet):
    """Custom ViewSet inheriting from BaseViewSet"""
    pass

class MyPermission(BasePermission):
    """Custom permission inheriting from BasePermission"""
    def check_permission(self, request, view):
        return request.user.is_staff
```

## Dependencies

- `djangorestframework` - REST API framework
- `django-extensions` - Django extensions
- `celery` - Asynchronous task processing

## Configuration

### Required Settings
```python
# settings.py
VERSION = '1.0.0'
APP_START_TIME = timezone.now()
HEALTH_CHECK_TIMEOUT = 5
```

### Environment Variables
```bash
# .env
VERSION=1.0.0
HEALTH_CHECK_TIMEOUT=5
```

## Best Practices

### Performance
- Cache health check results
- Use efficient database queries
- Implement proper error handling
- Monitor performance metrics

### Security
- Validate all inputs
- Implement proper authentication
- Use secure communication
- Log security events

### Code Quality
- Write comprehensive tests
- Use type hints
- Document all functions
- Follow DRY principles

## Troubleshooting

### Common Issues

1. **Health Check Failures**
   - Check service dependencies
   - Verify configuration
   - Review error logs
   - Test connectivity

2. **Exception Handling Issues**
   - Check exception handler configuration
   - Verify error logging
   - Review error responses
   - Test error scenarios

3. **Utility Function Errors**
   - Check input validation
   - Verify function logic
   - Review error handling
   - Test edge cases

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.core': {
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
