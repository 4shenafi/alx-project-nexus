"""
Basic tests to verify the setup works
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class BasicSetupTest(TestCase):
    """
    Test basic Django setup
    """

    def test_django_setup(self):
        """Test that Django is properly configured"""
        self.assertTrue(True)

    def test_user_model(self):
        """Test that custom user model is working"""
        user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="testpass123",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, "customer")


class HealthCheckTest(APITestCase):
    """
    Test health check endpoint
    """

    def test_health_check(self):
        """Test health check endpoint"""
        url = reverse("core:health_check")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "healthy")
