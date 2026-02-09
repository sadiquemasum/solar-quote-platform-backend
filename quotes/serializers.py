from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        fields = "__all__"

    # Field-level validation for monthly_bill
    def validate_monthly_bill(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Monthly bill must be greater than 0"
            )
        return value

    # Override create to calculate monthly_savings
    def create(self, validated_data):
        # Calculate monthly_savings on the backend
        monthly_bill = validated_data.get("monthly_bill", 0)
        validated_data["monthly_savings"] = int(monthly_bill * 0.3)  # e.g., 30% savings
        return super().create(validated_data)

class PublicQuoteSerializer(serializers.ModelSerializer):
    estimated_savings = serializers.SerializerMethodField()

    class Meta:
        model = Quote
        fields = [
            "id",
            "name",
            "email",
            "address",
            "monthly_bill",
            "estimated_savings",
            "created_at",
        ]

    def get_estimated_savings(self, obj):
        return round(obj.monthly_bill * 0.3, 2)
