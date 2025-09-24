# API Testing Guide

> **Step-by-step guide for testing the NexusCommerce API using Postman**

## Quick Start

### 1. Import Collection
1. Open Postman
2. Click "Import" and select `NexusCommerce_API_Collection.json`
3. Collection will be imported with all endpoints and built-in variables
4. No environment setup needed - everything is included!

### 2. API Server Information
The API is already running on the production server:
- **Base URL**: http://91.99.190.117:9090
- **API Documentation**: http://91.99.190.117:9090/api/v1/docs/
- **ReDoc Documentation**: http://91.99.190.117:9090/api/v1/redoc/
- **Admin Panel**: http://91.99.190.117:9090/admin/
- **Postman Collection**: [NexusCommerce API Collection](https://www.postman.com/ecommerce-app-dev-team/workspace/nexuscommerce-e-commerce-backend-api-s/collection/40062852-b625a321-bf63-4eeb-a53b-e5df30cb1bb5?action=share&creator=40062852)

### 3. Begin Testing
Start with the "Health Check" folder to verify your API is running.

## Complete Testing Workflow

### Phase 1: System Health Check
1. **Basic Health Check**
   - Endpoint: `GET /api/v1/health/`
   - Expected: 200 OK with status "healthy"

2. **Detailed Health Check**
   - Endpoint: `GET /api/v1/health/detailed/`
   - Expected: 200 OK with dependency status

### Phase 2: User Authentication Flow
1. **User Registration**
   - Endpoint: `POST /api/v1/auth/register/`
   - Body: Update email in request body
   - Expected: 201 Created with user data
   - Note: `user_id` is automatically stored

2. **Email Verification**
   - Endpoint: `POST /api/v1/auth/verify-email/`
   - Body: Use the email from registration
   - Expected: 200 OK with success message
   - Note: In development, check console for OTP

3. **User Login**
   - Endpoint: `POST /api/v1/auth/login/`
   - Body: Use registered email and password
   - Expected: 200 OK with tokens
   - Note: `access_token` and `refresh_token` are automatically stored

### Phase 3: User Profile Management
1. **Get User Profile**
   - Endpoint: `GET /api/v1/auth/profile/`
   - Expected: 200 OK with user profile data

2. **Update User Profile**
   - Endpoint: `PUT /api/v1/auth/profile/`
   - Body: Modify profile information
   - Expected: 200 OK with updated profile

3. **Create User Address**
   - Endpoint: `POST /api/v1/auth/addresses/`
   - Body: Add shipping/billing address
   - Expected: 201 Created with address data

### Phase 4: Product Catalog Testing
1. **List Categories**
   - Endpoint: `GET /api/v1/products/categories/`
   - Expected: 200 OK with category list

2. **List Products**
   - Endpoint: `GET /api/v1/products/`
   - Expected: 200 OK with paginated products

3. **Search Products**
   - Endpoint: `GET /api/v1/products/search/`
   - Query: Add search parameters
   - Expected: 200 OK with search results

4. **Get Product Details**
   - Endpoint: `GET /api/v1/products/1/`
   - Expected: 200 OK with product details
   - Note: `product_id` is automatically stored

5. **Get Product Variants**
   - Endpoint: `GET /api/v1/products/{{product_id}}/variants/`
   - Expected: 200 OK with variant list

### Phase 5: Shopping Cart Operations
1. **Get Cart**
   - Endpoint: `GET /api/v1/carts/`
   - Expected: 200 OK with cart data
   - Note: `cart_id` is automatically stored

2. **Add Item to Cart**
   - Endpoint: `POST /api/v1/carts/items/`
   - Body: Add product variant and quantity
   - Expected: 201 Created with cart item

3. **Get Cart Summary**
   - Endpoint: `GET /api/v1/carts/summary/`
   - Expected: 200 OK with totals and item count

4. **Update Cart Item**
   - Endpoint: `PUT /api/v1/carts/items/1/`
   - Body: Update quantity
   - Expected: 200 OK with updated item

5. **Validate Cart**
   - Endpoint: `POST /api/v1/carts/validate/`
   - Expected: 200 OK with validation results

### Phase 6: Order Processing
1. **Create Order**
   - Endpoint: `POST /api/v1/orders/`
   - Body: Use address IDs and payment method
   - Expected: 201 Created with order data
   - Note: `order_id` is automatically stored

2. **Get Order Details**
   - Endpoint: `GET /api/v1/orders/{{order_id}}/`
   - Expected: 200 OK with order details

3. **Get Order Items**
   - Endpoint: `GET /api/v1/orders/{{order_id}}/items/`
   - Expected: 200 OK with order items

4. **Update Order Status**
   - Endpoint: `PATCH /api/v1/orders/{{order_id}}/status/`
   - Body: Update status and add notes
   - Expected: 200 OK with updated order

### Phase 7: Payment Processing
1. **Get Payment Methods**
   - Endpoint: `GET /api/v1/payments/methods/`
   - Expected: 200 OK with payment methods

2. **Add Payment Method**
   - Endpoint: `POST /api/v1/payments/methods/`
   - Body: Add credit card or other payment method
   - Expected: 201 Created with payment method

3. **Create Payment**
   - Endpoint: `POST /api/v1/payments/`
   - Body: Use order ID and payment method
   - Expected: 201 Created with payment data
   - Note: `payment_id` is automatically stored

4. **Process Payment**
   - Endpoint: `POST /api/v1/payments/{{payment_id}}/process/`
   - Expected: 200 OK with processing result

5. **Get Payment Status**
   - Endpoint: `GET /api/v1/payments/{{payment_id}}/status/`
   - Expected: 200 OK with payment status

### Phase 8: Notification Management
1. **Get User Notifications**
   - Endpoint: `GET /api/v1/notifications/`
   - Expected: 200 OK with notification list

2. **Get Notification Preferences**
   - Endpoint: `GET /api/v1/notifications/preferences/`
   - Expected: 200 OK with user preferences

3. **Update Notification Preferences**
   - Endpoint: `PUT /api/v1/notifications/preferences/`
   - Body: Update notification settings
   - Expected: 200 OK with updated preferences

4. **Mark Notifications as Read**
   - Endpoint: `POST /api/v1/notifications/mark-read/`
   - Body: List of notification IDs
   - Expected: 200 OK with success message

### Phase 9: Admin Functions (Optional)
1. **List All Orders (Admin)**
   - Endpoint: `GET /api/v1/orders/admin/`
   - Expected: 200 OK with all orders (requires admin auth)

2. **Get Order Analytics (Admin)**
   - Endpoint: `GET /api/v1/orders/analytics/`
   - Expected: 200 OK with analytics data

3. **List Notification Templates (Admin)**
   - Endpoint: `GET /api/v1/notifications/templates/`
   - Expected: 200 OK with template list

## Testing Scenarios

### Happy Path Testing
Follow the complete workflow above to test the normal user journey from registration to order completion.

### Error Handling Testing
1. **Invalid Authentication**
   - Try accessing protected endpoints without token
   - Expected: 401 Unauthorized

2. **Invalid Data**
   - Send malformed request bodies
   - Expected: 400 Bad Request with validation errors

3. **Resource Not Found**
   - Access non-existent resources
   - Expected: 404 Not Found

4. **Permission Denied**
   - Try admin endpoints with regular user
   - Expected: 403 Forbidden

### Edge Case Testing
1. **Empty Cart Operations**
   - Try to checkout with empty cart
   - Expected: Appropriate error handling

2. **Invalid Product Variants**
   - Try to add non-existent variants to cart
   - Expected: 400 Bad Request

3. **Insufficient Stock**
   - Try to order more items than available
   - Expected: 400 Bad Request with stock error

4. **Expired Tokens**
   - Use expired access tokens
   - Expected: 401 Unauthorized

## Data Management

### Test Data Setup
1. **Create Test User**
   - Use unique email for each test run
   - Example: `test-{{$timestamp}}@example.com`

2. **Create Test Products**
   - Ensure products exist in database
   - Use management command: `python manage.py init_data`

3. **Clean Up After Testing**
   - Delete test orders and payments
   - Clear test user data if needed

### Built-in Variables
The collection includes all necessary variables:

#### Authentication Variables
- `access_token` - JWT access token (auto-set after login)
- `refresh_token` - JWT refresh token (auto-set after login)

#### ID Variables
- `user_id` - Current user ID (auto-set after registration)
- `order_id` - Last created order ID (auto-set after order creation)
- `product_id` - Last accessed product ID (auto-set after product operations)
- `cart_id` - Current cart ID (auto-set after cart operations)
- `payment_id` - Last created payment ID (auto-set after payment creation)

#### Test Data Variables
- `test_email` - Test user email (default: test@nexuscommerce.com)
- `test_password` - Test user password (default: name123)
- `admin_email` - Admin user email (default: admin@nexuscommerce.com)
- `admin_password` - Admin user password (default: name123)

#### Configuration Variables
- `base_url` - API base URL (default: http://91.99.190.117:9090)
- `api_version` - API version (default: v1)
- `shipping_address_id` - Default shipping address ID (default: 1)
- `billing_address_id` - Default billing address ID (default: 1)
- `payment_method_id` - Default payment method ID (default: 1)
- `product_variant_id` - Default product variant ID (default: 1)
- `category_id` - Default category ID (default: 1)
- `brand_id` - Default brand ID (default: 1)

## Performance Testing

### Load Testing
1. **Concurrent Requests**
   - Use Postman Runner with multiple iterations
   - Test with 10-50 concurrent requests

2. **Response Time Monitoring**
   - Check response times in Postman
   - Target: < 200ms for most endpoints

3. **Rate Limiting**
   - Test rate limit enforcement
   - Verify proper error responses

### Stress Testing
1. **High Volume Orders**
   - Create multiple orders simultaneously
   - Test database performance

2. **Large Cart Operations**
   - Add many items to cart
   - Test cart calculation performance

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Check if Django server is running
   - Verify port 8000 is available
   - Check firewall settings

2. **Authentication Errors**
   - Verify tokens are properly set
   - Check token expiration
   - Ensure correct user credentials

3. **Data Validation Errors**
   - Check request body format
   - Verify required fields are provided
   - Check data types and formats

4. **Permission Errors**
   - Verify user has required permissions
   - Check if user is properly authenticated
   - Ensure correct role assignments

### Debug Steps
1. **Check Response Headers**
   - Look for error details in headers
   - Check content-type and status codes

2. **Review Request Body**
   - Verify JSON format is correct
   - Check all required fields are present

3. **Validate Variables**
   - Ensure environment variables are set
   - Check variable values are correct

4. **Test Individual Endpoints**
   - Isolate problematic requests
   - Test with minimal data first

## Best Practices

### Testing Strategy
1. **Start Simple** - Begin with basic endpoints
2. **Build Up** - Progress to complex workflows
3. **Test Edge Cases** - Include error scenarios
4. **Verify Data** - Check response accuracy
5. **Clean Up** - Remove test data after testing

### Data Management
1. **Use Test Data** - Never use production data
2. **Isolate Tests** - Each test should be independent
3. **Clean Up** - Remove test data after completion
4. **Use Variables** - Store dynamic data in variables

### Documentation
1. **Document Issues** - Record any problems found
2. **Update Tests** - Keep tests current with API changes
3. **Share Results** - Communicate findings with team
4. **Maintain Collection** - Keep Postman collection updated

## Advanced Testing

### Automated Testing
1. **Postman Runner**
   - Use Runner for automated test execution
   - Set up test data and cleanup scripts

2. **Newman CLI**
   - Run collections from command line
   - Integrate with CI/CD pipelines

3. **Test Scripts**
   - Add validation scripts to requests
   - Automate response verification

### Integration Testing
1. **End-to-End Workflows**
   - Test complete user journeys
   - Verify data consistency across endpoints

2. **Cross-API Testing**
   - Test interactions between different APIs
   - Verify data flow and dependencies

3. **Error Propagation**
   - Test how errors propagate through system
   - Verify proper error handling

This testing guide provides a comprehensive approach to testing the NexusCommerce API. Follow the phases in order for a complete testing experience, or focus on specific areas as needed.
