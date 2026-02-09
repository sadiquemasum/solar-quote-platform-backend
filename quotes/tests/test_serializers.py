from django.test import TestCase
from quotes.models import Quote
from quotes.serializers import PublicQuoteSerializer
from quotes.serializers import QuoteSerializer

class PublicQuoteSerializerTest(TestCase):

    def test_estimated_savings_is_calculated_correctly(self):
        quote = Quote.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            address="Stockholm",
            monthly_bill=100
        )

        serializer = PublicQuoteSerializer(quote)
        data = serializer.data

        self.assertIn("estimated_savings", data)
        self.assertEqual(data["estimated_savings"], 30.0)

    def test_estimated_savings_rounding(self):
        quote = Quote.objects.create(
            name="John Doe",
            email="john@example.com",
            address="Uppsala",
            monthly_bill=123.45
        )

        serializer = PublicQuoteSerializer(quote)
        data = serializer.data

        self.assertEqual(data["estimated_savings"], round(123.45 * 0.3, 2))

    def test_negative_monthly_bill_is_invalid(self):
        data = {
            "name": "Bad Data",
            "email": "bad@example.com",
            "address": "Nowhere",
            "monthly_bill": -100,
        }

        serializer = QuoteSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("monthly_bill", serializer.errors)

    def test_zero_monthly_bill_is_invalid(self):
        data = {
            "name": "Zero Bill",
            "email": "zero@example.com",
            "address": "Stockholm",
            "monthly_bill": 0,
        }

        serializer = QuoteSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("monthly_bill", serializer.errors)

