# Notifications App - Multi-Channel Notification System

> **Comprehensive notification system supporting email, SMS, push notifications, and in-app messaging with template management**

## Overview

The Notifications app provides a unified notification system for NexusCommerce, supporting multiple communication channels including email, SMS, push notifications, and in-app messaging. It features template management, delivery tracking, and comprehensive analytics.

## Features

### Multi-Channel Support
- **Email Notifications**: HTML and text email templates with delivery tracking
- **SMS Notifications**: SMS messaging with delivery status tracking
- **Push Notifications**: Mobile and web push notifications
- **In-App Notifications**: Real-time in-app messaging system
- **Webhook Notifications**: Custom webhook integrations

### Template Management
- **Dynamic Templates**: Jinja2-based template system with variables
- **Template Categories**: Organized templates by notification type
- **Template Versioning**: Version control for template updates
- **Template Preview**: Live preview of templates with sample data
- **Multi-Language Support**: Localized templates for different languages

### Delivery Management
- **Delivery Tracking**: Real-time delivery status monitoring
- **Retry Logic**: Automatic retry for failed deliveries
- **Rate Limiting**: Configurable rate limiting per user/channel
- **Delivery Analytics**: Comprehensive delivery metrics and reporting
- **Bounce Handling**: Email bounce detection and management

### Notification Preferences
- **User Preferences**: Granular notification preferences per user
- **Channel Preferences**: User preferences for different channels
- **Frequency Control**: Notification frequency and timing controls
- **Opt-out Management**: Easy opt-out and unsubscribe handling

## Models

### NotificationTemplate Model
```python
class NotificationTemplate(models.Model):
    TEMPLATE_TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('in_app', 'In-App'),
        ('webhook', 'Webhook'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TEMPLATE_TYPE_CHOICES)
    category = models.CharField(max_length=50)
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    html_body = models.TextField(blank=True)
    variables = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    version = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Notification Model
```python
class Notification(models.Model):
    NOTIFICATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
    ]
    
    template = models.ForeignKey(NotificationTemplate, on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    channel = models.CharField(max_length=20, choices=NotificationTemplate.TEMPLATE_TYPE_CHOICES)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=NOTIFICATION_STATUS_CHOICES, default='pending')
    provider_id = models.CharField(max_length=255, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    opened_at = models.DateTimeField(null=True, blank=True)
    clicked_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### NotificationPreference Model
```python
class NotificationPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_preferences')
    category = models.CharField(max_length=50)
    channel = models.CharField(max_length=20, choices=NotificationTemplate.TEMPLATE_TYPE_CHOICES)
    is_enabled = models.BooleanField(default=True)
    frequency = models.CharField(max_length=20, default='immediate')
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'category', 'channel']
```

### NotificationLog Model
```python
class NotificationLog(models.Model):
    LOG_TYPE_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
        ('bounced', 'Bounced'),
        ('opened', 'Opened'),
        ('clicked', 'Clicked'),
        ('unsubscribed', 'Unsubscribed'),
    ]
    
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## API Endpoints

### Notifications
- `GET /api/v1/notifications/` - List user notifications
- `GET /api/v1/notifications/{id}/` - Get notification details
- `POST /api/v1/notifications/mark-read/` - Mark notifications as read
- `POST /api/v1/notifications/mark-all-read/` - Mark all notifications as read
- `DELETE /api/v1/notifications/{id}/` - Delete notification

### Templates (Admin)
- `GET /api/v1/notifications/templates/` - List notification templates
- `GET /api/v1/notifications/templates/{id}/` - Get template details
- `POST /api/v1/notifications/templates/` - Create template
- `PUT /api/v1/notifications/templates/{id}/` - Update template
- `DELETE /api/v1/notifications/templates/{id}/` - Delete template
- `POST /api/v1/notifications/templates/{id}/preview/` - Preview template

### Preferences
- `GET /api/v1/notifications/preferences/` - Get user preferences
- `PUT /api/v1/notifications/preferences/` - Update preferences
- `POST /api/v1/notifications/unsubscribe/` - Unsubscribe from notifications

### Analytics (Admin)
- `GET /api/v1/notifications/analytics/` - Get notification analytics
- `GET /api/v1/notifications/delivery-stats/` - Get delivery statistics

## Serializers

### NotificationSerializer
Notification serialization with status and delivery information.

### NotificationTemplateSerializer
Template serialization with variables and preview capabilities.

### NotificationPreferenceSerializer
User preference serialization with validation.

### NotificationLogSerializer
Log serialization for audit trails and analytics.

## Views

### NotificationViewSet
- User notification management
- Read/unread status tracking
- Notification deletion

### NotificationTemplateViewSet
- Template CRUD operations
- Template preview functionality
- Template versioning

### NotificationPreferenceViewSet
- User preference management
- Preference validation
- Opt-out handling

### NotificationAnalyticsView
- Delivery analytics
- Performance metrics
- User engagement statistics

## Notification Processing

### Send Notification
```python
def send_notification(template_name, recipient, context=None, channel=None, scheduled_at=None):
    """Send notification using template"""
    try:
        # Get template
        template = NotificationTemplate.objects.get(
            name=template_name,
            is_active=True
        )
        
        # Determine channel
        if not channel:
            channel = template.type
        
        # Check user preferences
        if not is_notification_allowed(recipient, template.category, channel):
            return None
        
        # Render template
        rendered_content = render_template(template, context or {})
        
        # Create notification
        notification = Notification.objects.create(
            template=template,
            recipient=recipient,
            channel=channel,
            subject=rendered_content.get('subject', ''),
            message=rendered_content.get('message', ''),
            scheduled_at=scheduled_at,
            metadata={'context': context or {}}
        )
        
        # Schedule or send immediately
        if scheduled_at and scheduled_at > timezone.now():
            schedule_notification.delay(notification.id, scheduled_at)
        else:
            send_notification_task.delay(notification.id)
        
        return notification
        
    except NotificationTemplate.DoesNotExist:
        raise TemplateNotFoundError(f"Template '{template_name}' not found")
    except Exception as e:
        raise NotificationError(f"Failed to send notification: {str(e)}")
```

### Template Rendering
```python
from jinja2 import Template, Environment

def render_template(template, context):
    """Render notification template with context"""
    env = Environment()
    
    # Render subject
    subject_template = Template(template.subject)
    subject = subject_template.render(context)
    
    # Render message
    message_template = Template(template.body)
    message = message_template.render(context)
    
    # Render HTML body if available
    html_message = None
    if template.html_body:
        html_template = Template(template.html_body)
        html_message = html_template.render(context)
    
    return {
        'subject': subject,
        'message': message,
        'html_message': html_message
    }
```

### Email Sending
```python
from django.core.mail import send_mail, EmailMultiAlternatives
from celery import shared_task

@shared_task
def send_email_notification(notification_id):
    """Send email notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Create email
        if notification.template.html_body:
            email = EmailMultiAlternatives(
                subject=notification.subject,
                body=notification.message,
                to=[notification.recipient.email]
            )
            email.attach_alternative(notification.message, "text/html")
        else:
            email = send_mail(
                subject=notification.subject,
                message=notification.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[notification.recipient.email],
                fail_silently=False
            )
        
        # Send email
        email.send()
        
        # Update notification status
        notification.status = 'sent'
        notification.sent_at = timezone.now()
        notification.save()
        
        # Log delivery
        NotificationLog.objects.create(
            notification=notification,
            log_type='sent',
            message='Email sent successfully'
        )
        
    except Exception as e:
        # Handle sending errors
        notification.status = 'failed'
        notification.save()
        
        NotificationLog.objects.create(
            notification=notification,
            log_type='failed',
            message=f'Email sending failed: {str(e)}',
            data={'error': str(e)}
        )
```

### SMS Sending
```python
import requests
from celery import shared_task

@shared_task
def send_sms_notification(notification_id):
    """Send SMS notification"""
    try:
        notification = Notification.objects.get(id=notification_id)
        
        # Send SMS via provider (example with Twilio)
        response = requests.post(
            f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json",
            auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
            data={
                'From': settings.TWILIO_PHONE_NUMBER,
                'To': notification.recipient.phone,
                'Body': notification.message
            }
        )
        
        if response.status_code == 201:
            notification.status = 'sent'
            notification.sent_at = timezone.now()
            notification.provider_id = response.json()['sid']
            notification.save()
            
            NotificationLog.objects.create(
                notification=notification,
                log_type='sent',
                message='SMS sent successfully',
                data=response.json()
            )
        else:
            raise Exception(f"SMS sending failed: {response.text}")
            
    except Exception as e:
        notification.status = 'failed'
        notification.save()
        
        NotificationLog.objects.create(
            notification=notification,
            log_type='failed',
            message=f'SMS sending failed: {str(e)}',
            data={'error': str(e)}
        )
```

## Preference Management

### Check Notification Permission
```python
def is_notification_allowed(user, category, channel):
    """Check if user allows notifications for category and channel"""
    try:
        preference = NotificationPreference.objects.get(
            user=user,
            category=category,
            channel=channel
        )
        return preference.is_enabled
    except NotificationPreference.DoesNotExist:
        # Default to enabled if no preference set
        return True
```

### Update User Preferences
```python
def update_notification_preferences(user, preferences):
    """Update user notification preferences"""
    for pref_data in preferences:
        preference, created = NotificationPreference.objects.update_or_create(
            user=user,
            category=pref_data['category'],
            channel=pref_data['channel'],
            defaults={
                'is_enabled': pref_data.get('is_enabled', True),
                'frequency': pref_data.get('frequency', 'immediate'),
                'quiet_hours_start': pref_data.get('quiet_hours_start'),
                'quiet_hours_end': pref_data.get('quiet_hours_end')
            }
        )
```

## Webhook Integration

### Delivery Status Webhooks
```python
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def email_webhook(request):
    """Handle email delivery status webhooks"""
    try:
        data = json.loads(request.body)
        event_type = data.get('event')
        
        if event_type == 'delivered':
            handle_email_delivered(data)
        elif event_type == 'bounced':
            handle_email_bounced(data)
        elif event_type == 'opened':
            handle_email_opened(data)
        elif event_type == 'clicked':
            handle_email_clicked(data)
        
        return HttpResponse(status=200)
        
    except Exception as e:
        logger.error(f"Email webhook error: {str(e)}")
        return HttpResponse(status=400)

def handle_email_delivered(data):
    """Handle email delivered webhook"""
    provider_id = data.get('message_id')
    try:
        notification = Notification.objects.get(provider_id=provider_id)
        notification.status = 'delivered'
        notification.delivered_at = timezone.now()
        notification.save()
        
        NotificationLog.objects.create(
            notification=notification,
            log_type='delivered',
            message='Email delivered successfully',
            data=data
        )
    except Notification.DoesNotExist:
        logger.warning(f"Notification not found for provider_id: {provider_id}")
```

## Testing

### Test Coverage
- Template rendering tests
- Notification sending tests
- Preference management tests
- Webhook handling tests
- Delivery tracking tests

### Test Commands
```bash
# Run all notification app tests
python manage.py test apps.notifications

# Run specific test module
python manage.py test apps.notifications.tests.test_models

# Run with coverage
coverage run --source=apps.notifications manage.py test apps.notifications
```

## Usage Examples

### Send Email Notification
```python
# Send welcome email
send_notification(
    template_name='welcome_email',
    recipient=user,
    context={
        'user_name': user.first_name,
        'login_url': 'https://example.com/login'
    }
)
```

### Send SMS Notification
```python
# Send order confirmation SMS
send_notification(
    template_name='order_confirmation_sms',
    recipient=user,
    context={
        'order_number': order.order_number,
        'total_amount': order.total_amount
    },
    channel='sms'
)
```

### Update User Preferences
```python
# Update notification preferences
data = {
    'preferences': [
        {
            'category': 'order_updates',
            'channel': 'email',
            'is_enabled': True,
            'frequency': 'immediate'
        },
        {
            'category': 'marketing',
            'channel': 'email',
            'is_enabled': False
        }
    ]
}
response = client.put('/api/v1/notifications/preferences/', data, headers=headers)
```

## Dependencies

- `celery` - Asynchronous task processing
- `jinja2` - Template rendering
- `requests` - HTTP requests for external APIs
- `djangorestframework` - REST API framework

## Configuration

### Required Settings
```python
# settings.py
DEFAULT_FROM_EMAIL = 'noreply@nexuscommerce.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'
```

### Environment Variables
```bash
# .env
DEFAULT_FROM_EMAIL=noreply@nexuscommerce.com
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

## Best Practices

### Performance
- Use asynchronous processing for notifications
- Implement proper rate limiting
- Cache frequently accessed templates
- Optimize database queries

### Security
- Validate all notification inputs
- Implement proper webhook verification
- Use secure communication channels
- Protect user privacy

### Code Quality
- Write comprehensive tests
- Use type hints
- Document all notification flows
- Implement proper error handling

## Troubleshooting

### Common Issues

1. **Email Not Sending**
   - Check email configuration
   - Verify SMTP settings
   - Check Celery worker status
   - Review email templates

2. **SMS Delivery Issues**
   - Check SMS provider configuration
   - Verify phone number format
   - Review SMS templates
   - Check provider limits

3. **Template Rendering Errors**
   - Check template syntax
   - Verify context variables
   - Review template variables
   - Test template rendering

### Debug Mode
```python
# Enable debug logging
LOGGING = {
    'loggers': {
        'apps.notifications': {
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
