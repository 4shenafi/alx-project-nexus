# API Testing Documentation

> **Comprehensive API testing collection for NexusCommerce e-commerce backend**

## Overview

This folder contains complete API testing resources for the NexusCommerce platform, including a comprehensive Postman collection and testing documentation.

## Files

### Postman Collection
- **`NexusCommerce_API_Collection.json`** - Complete all-in-one Postman collection with all API endpoints and built-in variables
- **`README.md`** - API testing documentation and setup guide
- **`Testing_Guide.md`** - Step-by-step testing workflow guide

## Postman Collection Features

### Complete API Coverage
- **Health Check Endpoints** - System health and status monitoring
- **Authentication** - User registration, login, logout, password reset
- **User Management** - Profile management, address handling
- **Products** - Product catalog, search, filtering, reviews
- **Shopping Cart** - Cart management, item operations
- **Orders** - Order creation, tracking, status updates
- **Payments** - Payment processing, refunds, payment methods
- **Notifications** - Notification management, preferences
- **Admin Endpoints** - Administrative functions and analytics

### Advanced Features
- **All-in-One Collection** - No separate environment files needed
- **Built-in Variables** - All variables included in the collection
- **Automatic Variable Management** - Tokens, IDs, and data automatically stored
- **Pre-request Scripts** - Automatic authentication and data setup
- **Test Scripts** - Response validation and variable extraction
- **Request Bodies** - Complete JSON payloads with variable substitution
- **Query Parameters** - All filtering and pagination options

## Setup Instructions

### 1. Import Collection
1. Open Postman
2. Click "Import" button
3. Select `NexusCommerce_API_Collection.json`
4. Collection will be imported with all endpoints and variables

### 2. Start Testing
1. No environment setup needed - all variables are built-in
2. Start with "Health Check" endpoints
3. Follow the authentication flow
4. Use other endpoints as needed

### 3. Customize Variables (Optional)
If you need to change default values, you can modify the collection variables:
- Right-click on the collection
- Select "Edit"
- Go to "Variables" tab
- Modify values as needed

## API Endpoints Overview

### Health Check
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/detailed/` - Detailed health check with dependencies

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/verify-email/` - Email verification
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Token refresh
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/password-reset/` - Password reset request
- `POST /api/v1/auth/password-reset-confirm/` - Password reset confirmation

### User Management
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT /api/v1/auth/profile/` - Update user profile
- `POST /api/v1/auth/change-password/` - Change password
- `GET /api/v1/auth/addresses/` - List user addresses
- `POST /api/v1/auth/addresses/` - Create user address

### Products
- `GET /api/v1/products/` - List products with filtering
- `GET /api/v1/products/search/` - Search products
- `GET /api/v1/products/{id}/` - Get product details
- `GET /api/v1/products/{id}/variants/` - Get product variants
- `GET /api/v1/products/{id}/reviews/` - Get product reviews
- `POST /api/v1/products/reviews/` - Create product review
- `GET /api/v1/products/categories/` - List categories

### Shopping Cart
- `GET /api/v1/carts/` - Get current cart
- `GET /api/v1/carts/summary/` - Get cart summary
- `POST /api/v1/carts/items/` - Add item to cart
- `PUT /api/v1/carts/items/{id}/` - Update cart item
- `DELETE /api/v1/carts/items/{id}/` - Remove cart item
- `POST /api/v1/carts/validate/` - Validate cart
- `DELETE /api/v1/carts/` - Clear cart

### Orders
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/` - List user orders
- `GET /api/v1/orders/{id}/` - Get order details
- `GET /api/v1/orders/{id}/items/` - Get order items
- `PATCH /api/v1/orders/{id}/status/` - Update order status
- `POST /api/v1/orders/{id}/cancel/` - Cancel order
- `GET /api/v1/orders/{id}/tracking/` - Get order tracking

### Payments
- `GET /api/v1/payments/methods/` - List payment methods
- `POST /api/v1/payments/methods/` - Add payment method
- `POST /api/v1/payments/` - Create payment
- `POST /api/v1/payments/{id}/process/` - Process payment
- `GET /api/v1/payments/{id}/` - Get payment details
- `GET /api/v1/payments/{id}/status/` - Get payment status
- `POST /api/v1/payments/refunds/` - Create refund
- `GET /api/v1/payments/refunds/` - List refunds

### Notifications
- `GET /api/v1/notifications/` - List user notifications
- `POST /api/v1/notifications/mark-read/` - Mark notifications as read
- `POST /api/v1/notifications/mark-all-read/` - Mark all as read
- `DELETE /api/v1/notifications/{id}/` - Delete notification
- `GET /api/v1/notifications/preferences/` - Get preferences
- `PUT /api/v1/notifications/preferences/` - Update preferences
- `POST /api/v1/notifications/unsubscribe/` - Unsubscribe

### Admin Endpoints
- `GET /api/v1/orders/admin/` - List all orders (Admin)
- `GET /api/v1/orders/analytics/` - Order analytics (Admin)
- `GET /api/v1/notifications/templates/` - List templates (Admin)
- `POST /api/v1/notifications/templates/` - Create template (Admin)
- `GET /api/v1/notifications/analytics/` - Notification analytics (Admin)

## Request Examples

### User Registration
```json
POST /api/v1/auth/register/
{
  "email": "test@example.com",
  "password": "SecurePass123!",
  "password_confirm": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

### Product Search
```json
GET /api/v1/products/search/?q=wireless headphones&category=1&min_price=50&max_price=200
```

### Add to Cart
```json
POST /api/v1/carts/items/
{
  "product_variant": 1,
  "quantity": 2
}
```

### Create Order
```json
POST /api/v1/orders/
{
  "shipping_address": 1,
  "billing_address": 1,
  "payment_method": "credit_card",
  "notes": "Please deliver during business hours"
}
```

### Process Payment
```json
POST /api/v1/payments/
{
  "order": 1,
  "payment_method": 1,
  "amount": "99.99"
}
```

## Authentication Flow

### 1. Register User
- Use "User Registration" endpoint
- User ID is automatically stored in variables

### 2. Verify Email
- Use "Email Verification" endpoint
- Provide OTP code from email

### 3. Login
- Use "User Login" endpoint
- Access and refresh tokens are automatically stored

### 4. Use Authenticated Endpoints
- All subsequent requests automatically include Bearer token
- Tokens are refreshed automatically when needed

## Variable Management

### Automatic Variables
The collection automatically manages these variables:
- `access_token` - JWT access token
- `refresh_token` - JWT refresh token
- `user_id` - Current user ID
- `order_id` - Last created order ID
- `product_id` - Last accessed product ID
- `cart_id` - Current cart ID
- `payment_id` - Last created payment ID

### Built-in Variables
All variables are included in the collection:
- `base_url` - API base URL (default: http://91.99.190.117:9090)
- `api_version` - API version (default: v1)
- `test_email` - Test user email (default: test@nexuscommerce.com)
- `test_password` - Test user password (default: name123)
- `admin_email` - Admin user email (default: admin@nexus.com)
- `admin_password` - Admin user password (default: admin123)
- `shipping_address_id` - Default shipping address ID (default: 1)
- `billing_address_id` - Default billing address ID (default: 1)
- `payment_method_id` - Default payment method ID (default: 1)
- `product_variant_id` - Default product variant ID (default: 1)
- `category_id` - Default category ID (default: 1)
- `brand_id` - Default brand ID (default: 1)

### Live API Endpoints
- **Base URL**: http://91.99.190.117:9090
- **API Documentation**: http://91.99.190.117:9090/api/v1/docs/
- **ReDoc Documentation**: http://91.99.190.117:9090/api/v1/redoc/
- **Admin Panel**: http://91.99.190.117:9090/admin/
- **Postman Collection**: [NexusCommerce API Collection](https://www.postman.com/ecommerce-app-dev-team/workspace/nexuscommerce-e-commerce-backend-api-s/collection/40062852-b625a321-bf63-4eeb-a53b-e5df30cb1bb5?action=share&creator=40062852)

## Testing Workflows

### Complete E-commerce Flow
1. **Health Check** - Verify API is running
2. **User Registration** - Create new user account
3. **Email Verification** - Verify email address
4. **User Login** - Authenticate user
5. **Browse Products** - Search and view products
6. **Add to Cart** - Add items to shopping cart
7. **Create Order** - Checkout and create order
8. **Process Payment** - Complete payment
9. **Track Order** - Monitor order status
10. **Manage Notifications** - Handle notifications

### Admin Testing Flow
1. **Login as Admin** - Use admin credentials
2. **View All Orders** - Access admin order management
3. **Order Analytics** - View order statistics
4. **Notification Templates** - Manage email templates
5. **System Analytics** - View system metrics

## Error Handling

### Common Error Responses
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Error Response Format
```json
{
  "error": "API Error",
  "message": "Detailed error message",
  "timestamp": "2025-01-27T10:30:00Z",
  "request_id": "unique-request-id",
  "details": {
    "field_name": ["Error message for specific field"]
  }
}
```

## Best Practices

### Testing Strategy
1. **Start with Health Checks** - Ensure API is accessible
2. **Follow Authentication Flow** - Complete user setup first
3. **Test Happy Path** - Verify normal operations work
4. **Test Error Cases** - Verify error handling
5. **Test Edge Cases** - Boundary conditions and limits

### Data Management
1. **Use Test Data** - Don't use production data
2. **Clean Up** - Remove test data after testing
3. **Isolate Tests** - Each test should be independent
4. **Use Variables** - Store dynamic data in variables

### Performance Testing
1. **Load Testing** - Test with multiple concurrent requests
2. **Response Time** - Monitor API response times
3. **Rate Limiting** - Test rate limit enforcement
4. **Error Rates** - Monitor error response rates

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Check if tokens are properly set
   - Verify token expiration
   - Ensure correct user credentials

2. **Connection Issues**
   - Verify base URL is correct
   - Check if API server is running
   - Test network connectivity

3. **Data Issues**
   - Verify required fields are provided
   - Check data format and types
   - Ensure valid IDs are used

4. **Permission Errors**
   - Verify user has required permissions
   - Check if user is authenticated
   - Ensure correct role assignments

### Debug Tips
1. **Check Response Headers** - Look for error details
2. **Review Request Body** - Verify data format
3. **Check Variables** - Ensure variables are set correctly
4. **Test Individual Endpoints** - Isolate problematic requests

## Contributing

### Adding New Endpoints
1. Follow existing naming conventions
2. Include proper request/response examples
3. Add appropriate test scripts
4. Update this documentation

### Improving Tests
1. Add more comprehensive test scripts
2. Include edge case testing
3. Add performance validation
4. Improve error handling tests

## License

This API testing collection is part of the NexusCommerce project and follows the same licensing terms.
