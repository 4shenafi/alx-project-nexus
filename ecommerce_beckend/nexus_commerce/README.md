# NexusCommerce Project Configuration

> **Main Django project configuration and settings for the NexusCommerce e-commerce platform**

## Overview

The `nexus_commerce` directory contains the main Django project configuration, settings, and core project files. This is the central configuration hub that orchestrates all the Django apps and defines the overall project structure.

## Project Structure

```
nexus_commerce/
├── __init__.py              # Project initialization
├── settings.py              # Main Django settings
├── urls.py                  # Main URL configuration
├── wsgi.py                  # WSGI configuration
├── asgi.py                  # ASGI configuration
├── celery.py                # Celery configuration
├── celery_beat_schedule.py  # Celery Beat schedule
└── README.md                # This documentation
```

## Configuration Files

### settings.py
The main Django settings file containing all project configuration:

#### Key Settings Sections:
- **Database Configuration**: PostgreSQL, Redis, and connection settings
- **Authentication**: JWT, user model, and security settings
- **API Configuration**: DRF settings, pagination, and API documentation
- **Celery Configuration**: Task queue and worker settings
- **Email Configuration**: SMTP and email backend settings
- **Security Settings**: CORS, CSRF, and security middleware
- **Static/Media Files**: File storage and serving configuration
- **Logging**: Comprehensive logging configuration
- **Environment Variables**: All configurable environment variables

#### Environment Variables:
```bash
# Core Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:password@localhost:5432/nexuscommerce

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=False
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# File Storage
MEDIA_ROOT=media
STATIC_ROOT=staticfiles

# Monitoring
SENTRY_DSN=

# Frontend
FRONTEND_URL=http://localhost:3000
```

### urls.py
Main URL configuration that routes requests to different apps:

```python
urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(), name='redoc'),
    
    # API v1 endpoints
    path('api/v1/', include('apps.core.urls')),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/products/', include('apps.products.urls')),
    path('api/v1/orders/', include('apps.orders.urls')),
    path('api/v1/carts/', include('apps.carts.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
]
```

### wsgi.py
WSGI configuration for production deployment:

```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_commerce.settings')
application = get_wsgi_application()
```

### asgi.py
ASGI configuration for asynchronous support:

```python
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_commerce.settings')
application = get_asgi_application()
```

### celery.py
Celery configuration for asynchronous task processing:

```python
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexus_commerce.settings')
app = Celery('nexus_commerce')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

### celery_beat_schedule.py
Celery Beat schedule for periodic tasks:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-daily-reports': {
        'task': 'apps.notifications.tasks.send_daily_reports',
        'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
    },
    'cleanup-expired-carts': {
        'task': 'apps.carts.tasks.cleanup_expired_carts',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'generate-monthly-analytics': {
        'task': 'apps.orders.tasks.generate_monthly_analytics',
        'schedule': crontab(0, 0, day_of_month=1),  # Monthly on 1st
    },
}
```

## Django Apps Configuration

### Installed Apps
The project includes the following Django apps:

```python
LOCAL_APPS = [
    'apps.core',           # Core utilities and base classes
    'apps.users',          # User management and authentication
    'apps.products',       # Product catalog management
    'apps.orders',         # Order processing and management
    'apps.carts',          # Shopping cart functionality
    'apps.payments',       # Payment processing
    'apps.notifications',  # Notification system
]
```

### Third-Party Apps
```python
THIRD_PARTY_APPS = [
    'rest_framework',                    # Django REST Framework
    'rest_framework_simplejwt',          # JWT authentication
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklisting
    'django_filters',                    # Advanced filtering
    'drf_spectacular',                   # API documentation
    'corsheaders',                       # CORS handling
    'django_ratelimit',                  # Rate limiting
    'django_extensions',                 # Django extensions
    'celery',                            # Asynchronous tasks
    'django_celery_beat',                # Periodic tasks
]
```

## Database Configuration

### PostgreSQL Setup
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='nexuscommerce'),
        'USER': env('DB_USER', default='postgres'),
        'PASSWORD': env('DB_PASSWORD', default='password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
        'OPTIONS': {
            'sslmode': 'prefer',
        },
    }
}
```

### Redis Configuration
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## API Configuration

### Django REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

### API Documentation
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'NexusCommerce API',
    'DESCRIPTION': 'Comprehensive e-commerce backend API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/v1/',
}
```

## Security Configuration

### JWT Settings
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=env('JWT_ACCESS_TOKEN_LIFETIME', default=60)),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=env('JWT_REFRESH_TOKEN_LIFETIME', default=1440)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env('SECRET_KEY'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

### Security Middleware
```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_ratelimit.middleware.RatelimitMiddleware',
]
```

## Logging Configuration

### Comprehensive Logging
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
```

## Development vs Production

### Development Settings
- Debug mode enabled
- Console email backend
- Local file storage
- Detailed error pages
- Development database

### Production Settings
- Debug mode disabled
- SMTP email backend
- Cloud storage (AWS S3)
- Security middleware enabled
- Production database with SSL

## Environment Management

### Environment Variables
All configuration is managed through environment variables using `django-environ`:

```python
import environ

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ''),
    DATABASE_URL=(str, ''),
    REDIS_URL=(str, ''),
    # ... other variables
)

environ.Env.read_env(BASE_DIR / '.env')
```

### Environment Files
- `.env` - Local development environment
- `.env.production` - Production environment
- `.env.staging` - Staging environment
- `env.example` - Example environment file

## Deployment Configuration

### Docker Support
The project includes Docker configuration for containerized deployment:

- `Dockerfile` - Application container
- `docker-compose.yml` - Multi-service setup
- `docker-compose.prod.yml` - Production configuration

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up Redis cluster
- [ ] Configure email backend
- [ ] Set up static file serving
- [ ] Configure SSL certificates
- [ ] Set up monitoring and logging
- [ ] Configure backup procedures

## Monitoring and Health Checks

### Health Check Endpoints
- `/api/v1/health/` - Basic health check
- `/api/v1/health/detailed/` - Detailed health check
- `/api/v1/status/` - Application status

### Monitoring Integration
- Sentry for error tracking
- Custom health check endpoints
- Performance monitoring
- Database query monitoring

## Best Practices

### Configuration Management
- Use environment variables for all configuration
- Separate development and production settings
- Use secure defaults
- Document all configuration options

### Security
- Use strong secret keys
- Enable security middleware
- Configure CORS properly
- Use HTTPS in production
- Regular security updates

### Performance
- Use database connection pooling
- Configure Redis caching
- Optimize database queries
- Use CDN for static files
- Monitor performance metrics

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Check database credentials
   - Verify database server status
   - Check network connectivity
   - Review connection pool settings

2. **Redis Connection Issues**
   - Check Redis server status
   - Verify Redis configuration
   - Check network connectivity
   - Review Redis memory usage

3. **Celery Issues**
   - Check Celery worker status
   - Verify broker configuration
   - Check task queue status
   - Review worker logs

4. **Email Issues**
   - Check SMTP configuration
   - Verify email credentials
   - Check firewall settings
   - Review email provider limits

### Debug Commands
```bash
# Check Django configuration
python manage.py check

# Check database connection
python manage.py dbshell

# Check Redis connection
python manage.py shell
>>> from django.core.cache import cache
>>> cache.set('test', 'ok')
>>> cache.get('test')

# Check Celery status
celery -A nexus_commerce inspect active

# Check environment variables
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEBUG)
```

## Contributing

1. Follow Django best practices
2. Use environment variables for configuration
3. Write comprehensive tests
4. Update documentation
5. Follow security guidelines

## License

This project is part of the NexusCommerce platform and follows the same licensing terms.
