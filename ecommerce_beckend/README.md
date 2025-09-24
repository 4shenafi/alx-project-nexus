<div align="center">

# NexusCommerce

### Enterprise-Grade E-commerce Backend Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.4-092e20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ed?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-dc382d?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)

---

**A modern, scalable, and production-ready e-commerce backend built with cutting-edge technologies**

</div>

## Quick Access

<div align="center">

### API Documentation & Testing

| Service | Link | Description |
|---------|------|-------------|
| **Swagger UI** | [![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black)](http://91.99.190.117:9090/api/v1/docs/) | Interactive API documentation |
| **ReDoc** | [![ReDoc](https://img.shields.io/badge/ReDoc-FF6B6B?style=for-the-badge&logo=readthedocs&logoColor=white)](http://91.99.190.117:9090/api/v1/redoc/) | Clean API reference |
| **Postman Collection** | [![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)](https://www.postman.com/ecommerce-app-dev-team/nexuscommerce-e-commerce-backend-api-s/collection/9ead4zj/nexuscommerce-complete-api-collection?action=share&creator=40062852) | Complete API test suite |

### Admin & Management

| Service | Link | Description |
|---------|------|-------------|
| **Django Admin** | [![Django Admin](https://img.shields.io/badge/Django%20Admin-092e20?style=for-the-badge&logo=django&logoColor=white)](http://91.99.190.117:9090/admin/) | Admin dashboard |
| **Health Check** | [![Health](https://img.shields.io/badge/Health%20Check-4CAF50?style=for-the-badge&logo=heart&logoColor=white)](http://91.99.190.117:9090/api/v1/health/) | System health status |

</div>

---

## Project Overview

NexusCommerce is a comprehensive e-commerce backend solution designed for modern businesses. Built with Django REST Framework, it provides a robust foundation for online retail operations with enterprise-grade features including real-time processing, advanced security, and seamless scalability.

### Key Features

<table>
<tr>
<td width="50%">

**Authentication & Security**
- JWT-based authentication
- Role-based access control
- Email verification with OTP
- Rate limiting & security headers
- Password strength validation

**E-commerce Core**
- Product catalog management
- Advanced search & filtering
- Shopping cart functionality
- Order processing workflow
- Inventory management

</td>
<td width="50%">

**Payment Integration**
- Multiple payment methods
- Secure transaction processing
- Refund management
- Payment status tracking
- Webhook handling

**Real-time Features**
- Live notifications
- Background task processing
- Email automation
- SMS integration
- Real-time updates

</td>
</tr>
</table>

## Architecture Overview

### Technology Stack

| Category | Technology | Version | Purpose |
|----------|------------|---------|---------|
| **Backend** | Django + DRF | 5.0.4 | Web framework & API |
| **Database** | PostgreSQL | 15+ | Primary data storage |
| **Cache** | Redis | 7+ | Caching & sessions |
| **Queue** | Celery | 5.3+ | Background tasks |
| **Auth** | JWT | SimpleJWT | Authentication |
| **Docs** | OpenAPI/Swagger | drf-spectacular | API documentation |
| **Container** | Docker | Latest | Containerization |
| **Testing** | pytest | Latest | Test framework |

### System Architecture

<div align="center">

[![System Architecture](https://drive.google.com/uc?export=view&id=1vt3kX84mAEUeTHQGVCb-mXKgl5PsDSBb)](https://drive.google.com/file/d/1vt3kX84mAEUeTHQGVCb-mXKgl5PsDSBb/view?usp=sharing)

*Click the diagram to view in full resolution*

</div>

### Production Features

<table>
<tr>
<td width="33%">

**Security**
- JWT Authentication
- Rate Limiting
- CORS Configuration
- Security Headers
- XSS Protection
- CSRF Protection

</td>
<td width="33%">

**Monitoring**
- Health Checks
- Structured Logging
- Error Tracking
- Performance Metrics
- Real-time Alerts
- System Status

</td>
<td width="33%">

**Performance**
- Redis Caching
- Database Optimization
- Background Processing
- Static File Serving
- CDN Integration
- Load Balancing

</td>
</tr>
</table>

## Project Structure

```
ecommerce_beckend/
├── apps/                          # Django applications
│   ├── core/                      # Core functionality & health checks
│   ├── users/                     # User management & authentication
│   ├── products/                  # Product catalog & inventory
│   ├── orders/                    # Order processing & management
│   ├── carts/                     # Shopping cart functionality
│   ├── payments/                  # Payment processing
│   └── notifications/             # Notification system
├── nexus_commerce/                # Project configuration
├── templates/                     # Email templates
├── api_testing/                   # API testing resources
├── tests/                         # Test suite
├── static/                        # Static files
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker configuration
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── .flake8                        # Flake8 configuration
├── .pre-commit-config.yaml        # Pre-commit hooks
├── pytest.ini                    # pytest configuration
└── manage.py                      # Django management script
```

## Application Documentation

### App-Specific Documentation
- [**Core App**](./apps/core/README.md) - Health checks and background tasks
- [**Users App**](./apps/users/README.md) - Authentication and user management
- [**Products App**](./apps/products/README.md) - Product catalog and inventory
- [**Orders App**](./apps/orders/README.md) - Order processing and management
- [**Carts App**](./apps/carts/README.md) - Shopping cart functionality
- [**Payments App**](./apps/payments/README.md) - Payment processing
- [**Notifications App**](./apps/notifications/README.md) - Notification system

### API Testing Documentation
- [**API Testing Guide**](./api_testing/README.md) - Comprehensive API testing
- [**Testing Guide**](./api_testing/Testing_Guide.md) - Step-by-step testing workflow
- [**Postman Collection**](./POSTMAN_COLLECTION.md) - Postman collection documentation

## Quick Start

### Prerequisites

| Requirement | Version | Installation |
|-------------|---------|--------------|
| **Python** | 3.11+ | [Download](https://python.org/downloads/) |
| **PostgreSQL** | 15+ | [Download](https://postgresql.org/download/) |
| **Redis** | 7+ | [Download](https://redis.io/download/) |
| **Docker** | Latest | [Download](https://docker.com/get-started/) |

### Installation Steps

<details>
<summary><b>1. Environment Setup</b></summary>

```bash
# Clone the repository
git clone https://github.com/4shenafi/alx-project-nexus.git
cd alx-project-nexus/ecommerce_beckend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

</details>

<details>
<summary><b>2. Environment Configuration</b></summary>

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
# Required variables:
# - SECRET_KEY
# - DATABASE_URL
# - REDIS_URL
# - EMAIL_HOST_USER
# - EMAIL_HOST_PASSWORD
```

**Required Environment Variables:**
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `EMAIL_HOST_USER` - SMTP email address
- `EMAIL_HOST_PASSWORD` - SMTP password

</details>

<details>
<summary><b>3. Database Setup</b></summary>

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Initialize sample data
python manage.py init_data
```

</details>

<details>
<summary><b>4. Start Development Server</b></summary>

```bash
# Start Django development server
python manage.py runserver

# In separate terminals, start Celery workers
celery -A nexus_commerce worker -l info
celery -A nexus_commerce beat -l info
```

**Access Points:**
- **API**: http://localhost:8000/api/v1/
- **Admin**: http://localhost:8000/admin/
- **Docs**: http://localhost:8000/api/v1/docs/

</details>

<details>
<summary><b>5. Docker Setup (Alternative)</b></summary>

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Docker Services:**
- **Web**: Django application
- **DB**: PostgreSQL database
- **Redis**: Cache and message broker
- **Celery**: Background task worker
- **Celery Beat**: Task scheduler

</details>

## API Endpoints Overview

### Authentication Endpoints
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `POST /api/v1/auth/verify-email/` - Email verification
- `POST /api/v1/auth/resend-otp/` - Resend verification OTP
- `POST /api/v1/auth/password-reset/` - Password reset request
- `POST /api/v1/auth/password-reset/confirm/` - Password reset confirmation
- `POST /api/v1/auth/change-password/` - Change password

### User Management
- `GET /api/v1/auth/profiles/` - List user profiles
- `GET /api/v1/auth/profiles/{id}/` - Get user profile
- `PATCH /api/v1/auth/profiles/{id}/` - Update user profile
- `GET /api/v1/auth/addresses/` - List user addresses
- `POST /api/v1/auth/addresses/` - Create user address
- `PUT /api/v1/auth/addresses/{id}/` - Update user address
- `DELETE /api/v1/auth/addresses/{id}/` - Delete user address

### Product Catalog
- `GET /api/v1/products/` - List products with filtering
- `GET /api/v1/products/{slug}/` - Get product details
- `POST /api/v1/products/` - Create product (vendors)
- `PUT /api/v1/products/{slug}/` - Update product (vendors)
- `DELETE /api/v1/products/{slug}/` - Delete product (vendors)
- `GET /api/v1/products/categories/` - List categories
- `GET /api/v1/products/brands/` - List brands
- `GET /api/v1/products/tags/` - List tags
- `GET /api/v1/products/reviews/` - List product reviews
- `POST /api/v1/products/reviews/` - Create product review

### Shopping Cart
- `GET /api/v1/carts/` - Get current cart
- `GET /api/v1/carts/summary/` - Get cart summary
- `POST /api/v1/carts/items/` - Add item to cart
- `PUT /api/v1/carts/items/{id}/` - Update cart item
- `DELETE /api/v1/carts/items/{id}/` - Remove cart item
- `POST /api/v1/carts/validate/` - Validate cart
- `DELETE /api/v1/carts/` - Clear cart

### Order Processing
- `POST /api/v1/orders/` - Create order
- `GET /api/v1/orders/` - List user orders
- `GET /api/v1/orders/{id}/` - Get order details
- `PATCH /api/v1/orders/{id}/status/` - Update order status
- `POST /api/v1/orders/{id}/cancel/` - Cancel order
- `GET /api/v1/orders/shipping-methods/` - List shipping methods

### Payment Processing
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

### System Health
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/detailed/` - Detailed health check

## CI/CD Pipeline

### GitHub Actions Workflow

Our project includes a comprehensive CI/CD pipeline that runs on every push and pull request:

#### Pipeline Stages

| Stage | Description | Status Badge |
|-------|-------------|--------------|
| **Tests** | Automated testing with PostgreSQL & Redis | [![Tests](https://github.com/4shenafi/alx-project-nexus/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/4shenafi/alx-project-nexus/actions) |
| **Linting** | Code quality checks (Black, isort, Flake8) | [![Linting](https://github.com/4shenafi/alx-project-nexus/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/4shenafi/alx-project-nexus/actions) |
| **Security** | Security scanning (Bandit, Safety) | [![Security](https://github.com/4shenafi/alx-project-nexus/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/4shenafi/alx-project-nexus/actions) |
| **Deployment** | Automatic deployment to VPS | [![Deployment](https://github.com/4shenafi/alx-project-nexus/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/4shenafi/alx-project-nexus/actions) |

#### Pipeline Features
- **Automated Testing**: Runs full test suite with PostgreSQL and Redis services
- **Code Quality**: Enforces PEP 8 compliance with Black, isort, and Flake8
- **Security Scanning**: Checks for vulnerabilities with Bandit and Safety
- **Coverage Reports**: Generates detailed test coverage reports
- **Auto Deployment**: Deploys to production VPS on main branch pushes

### View CI/CD Status
- **GitHub Actions**: [View Pipeline Runs](https://github.com/4shenafi/alx-project-nexus/actions) - See all green checkmarks ✅
- **Coverage Reports**: Available in Actions artifacts and Codecov
- **Deployment Logs**: Real-time deployment status in Actions
- **Live Deployment**: Production VPS automatically updated on successful builds

## Testing

### Test Coverage

Our comprehensive test suite ensures code quality and reliability:

```bash
# Run all tests with coverage
pytest --cov=apps

# View coverage report
open htmlcov/index.html
```

#### Coverage Features
- **Line-by-line Coverage**: Detailed coverage analysis
- **HTML Reports**: Interactive coverage reports in `htmlcov/index.html`
- **Coverage Thresholds**: Maintains high code coverage standards
- **CI Integration**: Coverage reports in GitHub Actions

### API Testing with Postman
1. **Import Collection**: Use the [NexusCommerce Complete API Collection](https://www.postman.com/ecommerce-app-dev-team/nexuscommerce-e-commerce-backend-api-s/collection/9ead4zj/nexuscommerce-complete-api-collection?action=share&creator=40062852)
2. **Follow Testing Guide**: [Step-by-Step Testing Guide](./api_testing/Testing_Guide.md)
3. **Test Complete Flow**: Registration → Login → Browse → Cart → Order → Payment

### Automated Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific test file
pytest tests/test_basic.py

# Run with verbose output
pytest -v

# Generate HTML coverage report
pytest --cov=apps --cov-report=html
```

### Running Tests Locally

To see the green "PASSED" results locally:

```bash
# Navigate to project directory
cd ecommerce_beckend

# Run test suite with coverage
pytest --cov=apps

# Expected output:
# ========================== test session starts ==========================
# platform linux -- Python 3.11.x, pytest-7.x.x, pluggy-1.x.x
# Django settings: nexus_commerce.settings (from ini file)
# plugins: django-4.x.x, cov-4.x.x
# collected 3 items
# 
# tests/test_basic.py::BasicSetupTest::test_django_setup PASSED    [ 33%]
# tests/test_basic.py::BasicSetupTest::test_user_model PASSED      [ 66%]
# tests/test_basic.py::HealthCheckTest::test_health_check PASSED   [100%]
# 
# ========================== 3 passed in 2.34s ==========================
# 
# ---------- coverage: platform linux, python 3.11.x -----------
# Name                    Stmts   Miss  Cover   Missing
# -----------------------------------------------------
# apps/core/views.py          15      0   100%
# apps/users/models.py       125      0   100%
# -----------------------------------------------------
# TOTAL                      140      0   100%
```

### View Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=apps --cov-report=html

# Open coverage report in browser
open htmlcov/index.html
```

The HTML report shows:
- **High-level coverage percentage** at the top
- **Line-by-line green highlighting** when hovering over files
- **Detailed coverage analysis** for each module

### Test Results
- **All Tests Passing**: ✅ Green checkmarks in CI/CD pipeline
- **High Coverage**: Comprehensive test coverage across all modules
- **Fast Execution**: Optimized test suite for quick feedback
- **Interactive Reports**: HTML coverage reports with line-by-line analysis

## Authentication

The API uses JWT (JSON Web Token) authentication:

1. **Register**: `POST /api/v1/auth/register/`
2. **Verify Email**: `POST /api/v1/auth/verify-email/`
3. **Login**: `POST /api/v1/auth/login/`
4. **Use Token**: Include `Authorization: Bearer <token>` in headers

### Example Authentication Flow
```bash
# 1. Register
curl -X POST http://91.99.190.117:9090/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
  }'

# 2. Verify email (check console for OTP)
curl -X POST http://91.99.190.117:9090/api/v1/auth/verify-email/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "otp": "123456"
  }'

# 3. Login
curl -X POST http://91.99.190.117:9090/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'

# 4. Use authenticated endpoint
curl -X GET http://91.99.190.117:9090/api/v1/auth/profiles/ \
  -H "Authorization: Bearer <your-access-token>"
```

## Deployment

### Production VPS Deployment

Our application is deployed on a production VPS with automated CI/CD:

#### Production Status
- **Environment**: Production VPS
- **Port**: 9090 (Production API)
- **Status**: Live and operational
- **Auto-Deploy**: Enabled via GitHub Actions

#### Live Services
| Service | URL | Status |
|---------|-----|--------|
| **API** | http://91.99.190.117:9090/api/v1/ | 🟢 Live |
| **Swagger** | http://91.99.190.117:9090/api/v1/docs/ | 🟢 Live |
| **Admin** | http://91.99.190.117:9090/admin/ | 🟢 Live |
| **Health** | http://91.99.190.117:9090/api/v1/health/ | 🟢 Live |

#### Deployment Process
1. **Push to Main**: Triggers automatic deployment
2. **CI/CD Pipeline**: Runs tests, linting, and security checks
3. **VPS Deployment**: Automatically deploys to production server
4. **Health Check**: Verifies deployment success

### Docker Deployment

#### Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

#### Automated Deployment
The production deployment is fully automated via GitHub Actions:

1. **Push to Main Branch** → Triggers CI/CD pipeline
2. **Run Tests & Quality Checks** → Ensures code quality
3. **Deploy to Production** → Automatic deployment to VPS
4. **Health Check** → Verifies successful deployment

**View Deployment Status**: [GitHub Actions](https://github.com/4shenafi/alx-project-nexus/actions)

#### Manual Deployment Commands
```bash
# Build production image
docker build -t nexuscommerce-backend .

# Run with production settings
docker run -d \
  --name nexuscommerce-backend \
  -p 9090:8000 \
  -e DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgres://user:pass@db:5432/nexuscommerce \
  -e REDIS_URL=redis://redis:6379/0 \
  nexuscommerce-backend
```

## Background Tasks

The system uses Celery for asynchronous task processing:

### Scheduled Tasks
- **Session Cleanup**: Hourly expired session cleanup
- **Low Stock Alerts**: Daily vendor notifications
- **Search Index Updates**: Daily product search optimization
- **Vendor Reports**: Monthly sales reports
- **Order Processing**: Every 5 minutes pending order checks
- **Notification Cleanup**: Weekly old notification cleanup

### Async Tasks
- **Email Sending**: Transactional emails
- **Image Processing**: Thumbnail generation
- **Report Generation**: Vendor analytics
- **Order Fulfillment**: Inventory updates and notifications

## Monitoring & Health Checks

### Health Check Endpoints
- **Basic Health**: `GET /api/v1/health/`
- **Detailed Health**: `GET /api/v1/health/detailed/`

### Health Check Response
```json
{
  "status": "healthy",
  "checks": {
    "database": true,
    "cache": true,
    "celery": true
  },
  "version": "1.0.0"
}
```

## Security Features

### Authentication & Authorization
- JWT-based authentication with refresh tokens
- Role-based access control (Customer, Vendor, Admin)
- Rate limiting on sensitive endpoints
- Email verification with OTP
- Password strength validation

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- XSS protection headers
- CSRF protection
- Secure session management

### API Security
- CORS configuration
- Request/response validation
- Error handling without information leakage
- Secure file upload handling

## Performance Features

### Caching Strategy
- Redis for session storage
- Database query caching
- Static file caching
- API response caching

### Database Optimization
- Strategic indexing
- Query optimization with select_related/prefetch_related
- Database connection pooling
- Efficient pagination

### Background Processing
- Asynchronous email sending
- Image processing
- Report generation
- Data cleanup tasks

## Configuration

### Environment Variables
See `.env.example` for all available configuration options:

```bash
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DATABASE_URL=postgres://user:password@localhost:5432/nexuscommerce_db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### Project Configuration
- [**Project Configuration**](./nexus_commerce/README.md) - Django project settings

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and ensure tests pass
4. Commit your changes: `git commit -m 'Add amazing feature'`
5. Push to the branch: `git push origin feature/amazing-feature`
6. Open a Pull Request

## License

This project is part of the ALX ProDev Backend Engineering program and follows the same licensing terms.

## Support

For technical support or questions:
- **GitHub Issues**: [Create an issue](https://github.com/4shenafi/alx-project-nexus/issues)
- **Email**: ashenafipawlos939@gmail.com
- **LinkedIn**: [4shenafi](https://www.linkedin.com/in/4shenafi/)

---

<div align="center">

**Built with ❤️ for the ALX ProDev Backend Engineering program**

*Last Updated: September 2025*

</div>