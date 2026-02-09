from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from quotes.models import Quote


class QuoteAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and token for dashboard tests
        self.user = User.objects.create_user(username="admin", password="password123")
        self.token = Token.objects.create(user=self.user)

        # URLs
        self.quote_create_url = reverse("quote-create")
        self.dashboard_url = reverse("dashboard-quotes")

    # ----------------------------
    # Public quote submission tests
    # ----------------------------
    def test_create_quote_success(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "address": "Stockholm",
            "monthly_bill": 100,
        }
        response = self.client.post(self.quote_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quote.objects.count(), 1)

    def test_create_quote_success_check_calculation(self):
        payload = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "address": "Stockholm",
            "monthly_bill": 100,
        }
        response = self.client.post(self.quote_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["monthly_savings"], 30)  #check calculation

    def test_create_quote_invalid(self):
        payload = {
            "name": "Bad Data",
            "email": "bad@example.com",
            "address": "Nowhere",
            "monthly_bill": -50,
        }
        response = self.client.post(self.quote_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("monthly_bill", response.data)

    # ----------------------------
    # Dashboard / token auth tests
    # ----------------------------
    def test_dashboard_no_token_returns_401(self):
        # No credentials
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_invalid_token_returns_401(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token invalidtoken123")
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_valid_token_returns_200(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        # Create a quote to verify data is returned
        Quote.objects.create(
            name="John Doe",
            email="john@example.com",
            address="Uppsala",
            monthly_bill=120,
        )
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["email"], "john@example.com")

