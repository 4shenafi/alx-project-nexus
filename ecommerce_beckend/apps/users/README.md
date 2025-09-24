# Users App - Authentication & User Management

> **Comprehensive user authentication, authorization, and profile management system for NexusCommerce**

## Overview

The Users app handles all aspects of user management including registration, authentication, authorization, profile management, and role-based access control. It implements industry-standard security practices with JWT tokens, email verification, and comprehensive permission systems.

## Features

### Authentication System
- **User Registration**: Email-based registration with OTP verification
- **Login/Logout**: Secure JWT-based authentication
- **Password Management**: Reset, change, and validation
- **Email Verification**: OTP-based email verification system
- **Token Management**: JWT access and refresh tokens with blacklisting

### User Management
- **Profile Management**: Complete user profile with avatar support
- **Role-Based Access Control**: Customer, Vendor, Admin roles
- **User Status**: Active, inactive, and suspended states
- **Address Management**: Multiple shipping and billing addresses

### Security Features
- **JWT Authentication**: Secure token-based authentication
- **Permission Classes**: Custom permission classes for different access levels
- **Rate Limiting**: Built-in rate limiting for authentication endpoints
- **Password Validation**: Strong password requirements
- **Account Security**: Login attempt tracking and account lockout

## Models

### User Model
```python
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    is_verified = models.BooleanField(default=False)
    is_vendor_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Address Model
```python
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/verify-email/` - Email verification with OTP
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/refresh/` - Token refresh
- `POST /api/v1/auth/password-reset/` - Password reset request
- `POST /api/v1/auth/password-reset-confirm/` - Password reset confirmation

### User Management
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT /api/v1/auth/profile/` - Update user profile
- `POST /api/v1/auth/change-password/` - Change password
- `GET /api/v1/auth/addresses/` - List user addresses
- `POST /api/v1/auth/addresses/` - Create new address
- `PUT /api/v1/auth/addresses/{id}/` - Update address
- `DELETE /api/v1/auth/addresses/{id}/` - Delete address

## Permission Classes

### IsOwner
Allows access only to the owner of the resource.

### IsAdminUser
Allows access only to admin users.

### IsApprovedVendor
Allows access only to approved vendors.

## Serializers

### UserRegistrationSerializer
Handles user registration with email validation and password confirmation.

### UserLoginSerializer
Manages user login with email/password authentication.

### UserProfileSerializer
Serializes user profile data including avatar and role information.

### AddressSerializer
Handles address creation and updates with validation.

## Views

### UserRegistrationView
- Handles user registration
- Sends OTP verification email
- Creates unverified user account

### EmailVerificationView
- Verifies OTP code
- Activates user account
- Sends welcome email

### UserLoginView
- Authenticates user credentials
- Returns JWT tokens
- Updates last login timestamp

### UserProfileView
- Retrieves and updates user profile
- Handles avatar upload
- Manages user preferences

### AddressViewSet
- CRUD operations for user addresses
- Manages default address selection
- Validates address data

## Security Implementation

### JWT Configuration
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

### Password Validation
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character

### Rate Limiting
- Login attempts: 5 per minute
- Registration: 3 per hour
- Password reset: 3 per hour

## Email Templates

### Registration Email
- Welcome message
- OTP verification code
- Account activation instructions

### Password Reset Email
- Reset link with token
- Security instructions
- Expiration notice

## Testing

### Test Coverage
- Unit tests for all models
- Integration tests for API endpoints
- Authentication flow testing
- Permission class testing
- Email functionality testing

### Test Commands
```bash
# Run all user app tests
python manage.py test apps.users

# Run specific test module
python manage.py test apps.users.tests.test_models

# Run with coverage
coverage run --source=apps.users manage.py test apps.users
```

## Usage Examples

### User Registration
```python
# Register new user
data = {
    'email': 'user@example.com',
    'password': 'SecurePass123!',
    'password_confirm': 'SecurePass123!',
    'first_name': 'John',
    'last_name': 'Doe'
}
response = client.post('/api/v1/auth/register/', data)
```

### User Login
```python
# Login user
data = {
    'email': 'user@example.com',
    'password': 'SecurePass123!'
}
response = client.post('/api/v1/auth/login/', data)
tokens = response.data['tokens']
```

### Profile Update
```python
# Update user profile
headers = {'Authorization': f'Bearer {access_token}'}
data = {
    'first_name': 'John',
    'last_name': 'Smith',
    'phone': '+1234567890'
}
response = client.put('/api/v1/auth/profile/', data, headers=headers)
```

## Dependencies

- `djangorestframework` - REST API framework
- `djangorestframework-simplejwt` - JWT authentication
- `django-ratelimit` - Rate limiting
- `Pillow` - Image handling for avatars
- `celery` - Asynchronous email sending

## Configuration

### Required Settings
```python
# settings.py
AUTH_USER_MODEL = 'users.User'
SIMPLE_JWT = {...}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

### Environment Variables
```bash
# .env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Best Practices

### Security
- Always use HTTPS in production
- Implement proper CORS settings
- Use strong password requirements
- Regular security audits
- Monitor failed login attempts

### Performance
- Use database indexes on frequently queried fields
- Implement caching for user sessions
- Optimize database queries
- Use select_related for foreign keys

### Code Quality
- Follow PEP 8 standards
- Write comprehensive tests
- Use type hints
- Document all public methods
- Implement proper error handling

## Troubleshooting

### Common Issues

1. **JWT Token Expired**
   - Use refresh token to get new access token
   - Implement automatic token refresh

2. **Email Not Sending**
   - Check email configuration
   - Verify SMTP settings
   - Check Celery worker status

3. **Permission Denied**
   - Verify user role and permissions
   - Check token validity
   - Ensure proper authentication headers

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.users': {
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
