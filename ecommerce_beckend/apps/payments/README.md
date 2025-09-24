# Payments App - Payment Processing System

> **Comprehensive payment processing system with multiple payment methods, secure transactions, and refund management**

## Overview

The Payments app handles all payment processing for NexusCommerce, including payment method management, transaction processing, refund handling, and payment analytics. It integrates with multiple payment providers and implements secure payment processing with PCI compliance considerations.

## Features

### Payment Processing
- **Multiple Payment Methods**: Credit cards, PayPal, bank transfers, digital wallets
- **Secure Transactions**: PCI-compliant payment processing
- **Payment Validation**: Real-time payment validation and verification
- **Transaction Logging**: Comprehensive transaction history and audit trail
- **Payment Status Tracking**: Real-time payment status updates
- **Fraud Detection**: Basic fraud detection and prevention

### Refund Management
- **Refund Processing**: Full and partial refund capabilities
- **Refund Tracking**: Complete refund history and status tracking
- **Refund Analytics**: Refund patterns and analysis
- **Automated Refunds**: Automated refund processing for specific conditions

### Payment Analytics
- **Transaction Analytics**: Payment volume and success rate analysis
- **Revenue Tracking**: Revenue analytics and reporting
- **Payment Method Analytics**: Performance analysis by payment method
- **Fraud Analytics**: Fraud detection metrics and reporting

## Models

### PaymentMethod Model
```python
class PaymentMethod(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('digital_wallet', 'Digital Wallet'),
        ('crypto', 'Cryptocurrency'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    provider = models.CharField(max_length=50)  # stripe, paypal, etc.
    provider_payment_method_id = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Payment Model
```python
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    provider_transaction_id = models.CharField(max_length=255, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    failure_reason = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Refund Model
```python
class Refund(models.Model):
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='refunds')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    provider_refund_id = models.CharField(max_length=255, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### TransactionLog Model
```python
class TransactionLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('payment_created', 'Payment Created'),
        ('payment_processed', 'Payment Processed'),
        ('payment_failed', 'Payment Failed'),
        ('refund_created', 'Refund Created'),
        ('refund_processed', 'Refund Processed'),
        ('webhook_received', 'Webhook Received'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## API Endpoints

### Payment Methods
- `GET /api/v1/payments/methods/` - List user payment methods
- `POST /api/v1/payments/methods/` - Add new payment method
- `PUT /api/v1/payments/methods/{id}/` - Update payment method
- `DELETE /api/v1/payments/methods/{id}/` - Remove payment method
- `POST /api/v1/payments/methods/{id}/set-default/` - Set default payment method

### Payments
- `GET /api/v1/payments/` - List user payments
- `GET /api/v1/payments/{id}/` - Get payment details
- `POST /api/v1/payments/` - Create payment
- `POST /api/v1/payments/{id}/process/` - Process payment
- `POST /api/v1/payments/{id}/cancel/` - Cancel payment
- `GET /api/v1/payments/{id}/status/` - Get payment status

### Refunds
- `GET /api/v1/payments/refunds/` - List refunds
- `GET /api/v1/payments/refunds/{id}/` - Get refund details
- `POST /api/v1/payments/refunds/` - Create refund
- `POST /api/v1/payments/refunds/{id}/process/` - Process refund

### Webhooks
- `POST /api/v1/payments/webhooks/stripe/` - Stripe webhook endpoint
- `POST /api/v1/payments/webhooks/paypal/` - PayPal webhook endpoint

## Serializers

### PaymentMethodSerializer
Payment method serialization with secure data handling.

### PaymentSerializer
Payment serialization with transaction details and status.

### RefundSerializer
Refund serialization with processing information.

### TransactionLogSerializer
Transaction log serialization for audit trails.

## Views

### PaymentMethodViewSet
- Payment method CRUD operations
- Default payment method management
- Payment method validation

### PaymentViewSet
- Payment creation and processing
- Payment status management
- Payment history and tracking

### RefundViewSet
- Refund creation and processing
- Refund status management
- Refund analytics

### WebhookView
- Payment provider webhook handling
- Webhook verification and processing
- Event logging and tracking

## Payment Processing

### Payment Creation
```python
@transaction.atomic
def create_payment(order, payment_method, amount):
    """Create payment with validation"""
    # Validate payment method
    if not payment_method.is_active:
        raise PaymentMethodInactiveError("Payment method is not active")
    
    # Validate amount
    if amount <= 0:
        raise InvalidAmountError("Payment amount must be positive")
    
    # Create payment
    payment = Payment.objects.create(
        order=order,
        payment_method=payment_method,
        amount=amount,
        currency=order.currency,
        status='pending'
    )
    
    # Log payment creation
    TransactionLog.objects.create(
        payment=payment,
        log_type='payment_created',
        message=f'Payment created for order {order.order_number}',
        data={'amount': str(amount), 'currency': order.currency}
    )
    
    return payment
```

### Payment Processing
```python
def process_payment(payment):
    """Process payment through provider"""
    try:
        # Update status to processing
        payment.status = 'processing'
        payment.save()
        
        # Process based on payment method type
        if payment.payment_method.type == 'credit_card':
            result = process_credit_card_payment(payment)
        elif payment.payment_method.type == 'paypal':
            result = process_paypal_payment(payment)
        else:
            raise UnsupportedPaymentMethodError(f"Unsupported payment method: {payment.payment_method.type}")
        
        # Update payment with result
        payment.provider_transaction_id = result['transaction_id']
        payment.provider_response = result['response']
        payment.status = 'completed' if result['success'] else 'failed'
        payment.processed_at = timezone.now()
        payment.failure_reason = result.get('error_message', '')
        payment.save()
        
        # Log transaction
        TransactionLog.objects.create(
            payment=payment,
            log_type='payment_processed' if result['success'] else 'payment_failed',
            message=result['message'],
            data=result['response']
        )
        
        return result
        
    except Exception as e:
        # Handle processing errors
        payment.status = 'failed'
        payment.failure_reason = str(e)
        payment.save()
        
        TransactionLog.objects.create(
            payment=payment,
            log_type='payment_failed',
            message=f'Payment processing failed: {str(e)}',
            data={'error': str(e)}
        )
        
        raise PaymentProcessingError(f"Payment processing failed: {str(e)}")
```

### Stripe Integration
```python
import stripe

def process_credit_card_payment(payment):
    """Process credit card payment through Stripe"""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    try:
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Convert to cents
            currency=payment.currency.lower(),
            payment_method=payment.payment_method.provider_payment_method_id,
            confirmation_method='manual',
            confirm=True,
            metadata={
                'order_id': payment.order.id,
                'payment_id': payment.id
            }
        )
        
        if intent.status == 'succeeded':
            return {
                'success': True,
                'transaction_id': intent.id,
                'response': intent,
                'message': 'Payment completed successfully'
            }
        else:
            return {
                'success': False,
                'transaction_id': intent.id,
                'response': intent,
                'error_message': f'Payment failed: {intent.status}',
                'message': 'Payment processing failed'
            }
            
    except stripe.error.CardError as e:
        return {
            'success': False,
            'response': {'error': str(e)},
            'error_message': str(e),
            'message': 'Card payment failed'
        }
    except Exception as e:
        return {
            'success': False,
            'response': {'error': str(e)},
            'error_message': str(e),
            'message': 'Payment processing error'
        }
```

## Refund Processing

### Refund Creation
```python
@transaction.atomic
def create_refund(payment, amount, reason, processed_by=None):
    """Create refund with validation"""
    # Validate refund amount
    if amount <= 0:
        raise InvalidAmountError("Refund amount must be positive")
    
    # Check if refund amount exceeds payment amount
    total_refunded = payment.refunds.filter(status='completed').aggregate(
        total=models.Sum('amount')
    )['total'] or 0
    
    if total_refunded + amount > payment.amount:
        raise InvalidRefundAmountError("Refund amount exceeds payment amount")
    
    # Create refund
    refund = Refund.objects.create(
        payment=payment,
        amount=amount,
        reason=reason,
        status='pending',
        processed_by=processed_by
    )
    
    return refund
```

### Refund Processing
```python
def process_refund(refund):
    """Process refund through provider"""
    try:
        # Update status to processing
        refund.status = 'processing'
        refund.save()
        
        # Process based on payment method
        if refund.payment.payment_method.type == 'credit_card':
            result = process_stripe_refund(refund)
        elif refund.payment.payment_method.type == 'paypal':
            result = process_paypal_refund(refund)
        else:
            raise UnsupportedPaymentMethodError(f"Unsupported payment method for refund: {refund.payment.payment_method.type}")
        
        # Update refund with result
        refund.provider_refund_id = result['refund_id']
        refund.provider_response = result['response']
        refund.status = 'completed' if result['success'] else 'failed'
        refund.processed_at = timezone.now()
        refund.save()
        
        # Update payment status if fully refunded
        if refund.status == 'completed':
            total_refunded = refund.payment.refunds.filter(status='completed').aggregate(
                total=models.Sum('amount')
            )['total'] or 0
            
            if total_refunded >= refund.payment.amount:
                refund.payment.status = 'refunded'
            else:
                refund.payment.status = 'partially_refunded'
            refund.payment.save()
        
        return result
        
    except Exception as e:
        refund.status = 'failed'
        refund.save()
        raise RefundProcessingError(f"Refund processing failed: {str(e)}")
```

## Webhook Handling

### Stripe Webhook
```python
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook events"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        handle_payment_succeeded(event['data']['object'])
    elif event['type'] == 'payment_intent.payment_failed':
        handle_payment_failed(event['data']['object'])
    elif event['type'] == 'charge.dispute.created':
        handle_charge_dispute(event['data']['object'])
    
    return HttpResponse(status=200)

def handle_payment_succeeded(payment_intent):
    """Handle successful payment webhook"""
    try:
        payment = Payment.objects.get(
            provider_transaction_id=payment_intent['id']
        )
        payment.status = 'completed'
        payment.processed_at = timezone.now()
        payment.save()
        
        # Update order status
        payment.order.status = 'confirmed'
        payment.order.save()
        
    except Payment.DoesNotExist:
        logger.error(f"Payment not found for Stripe payment intent: {payment_intent['id']}")
```

## Testing

### Test Coverage
- Payment creation and processing tests
- Refund creation and processing tests
- Webhook handling tests
- Payment method management tests
- Transaction logging tests

### Test Commands
```bash
# Run all payment app tests
python manage.py test apps.payments

# Run specific test module
python manage.py test apps.payments.tests.test_models

# Run with coverage
coverage run --source=apps.payments manage.py test apps.payments
```

## Usage Examples

### Create Payment
```python
# Create payment
data = {
    'order': 1,
    'payment_method': 1,
    'amount': '99.99'
}
response = client.post('/api/v1/payments/', data, headers=headers)
payment = response.data
```

### Process Payment
```python
# Process payment
response = client.post('/api/v1/payments/1/process/', headers=headers)
result = response.data
```

### Create Refund
```python
# Create refund
data = {
    'payment': 1,
    'amount': '50.00',
    'reason': 'Customer requested refund'
}
response = client.post('/api/v1/payments/refunds/', data, headers=headers)
refund = response.data
```

## Dependencies

- `stripe` - Stripe payment processing
- `paypalrestsdk` - PayPal payment processing
- `djangorestframework` - REST API framework
- `celery` - Asynchronous task processing

## Configuration

### Required Settings
```python
# settings.py
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
STRIPE_WEBHOOK_SECRET = 'whsec_...'
PAYPAL_CLIENT_ID = 'your_paypal_client_id'
PAYPAL_CLIENT_SECRET = 'your_paypal_client_secret'
```

### Environment Variables
```bash
# .env
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
```

## Security Considerations

### PCI Compliance
- Never store credit card details
- Use tokenized payment methods
- Implement proper access controls
- Regular security audits

### Data Protection
- Encrypt sensitive payment data
- Implement proper logging
- Use secure communication channels
- Regular backup procedures

## Best Practices

### Performance
- Use asynchronous processing for payments
- Implement proper error handling
- Use database transactions
- Cache frequently accessed data

### Security
- Validate all payment inputs
- Implement fraud detection
- Use secure webhook verification
- Regular security updates

### Code Quality
- Write comprehensive tests
- Use type hints
- Document all payment flows
- Implement proper error handling

## Troubleshooting

### Common Issues

1. **Payment Processing Failures**
   - Check payment provider configuration
   - Verify webhook endpoints
   - Review error logs
   - Check network connectivity

2. **Webhook Issues**
   - Verify webhook signatures
   - Check endpoint accessibility
   - Review webhook logs
   - Test webhook delivery

3. **Refund Processing Issues**
   - Check refund policies
   - Verify payment status
   - Review provider limits
   - Check refund eligibility

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.payments': {
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
