from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import *


class CustomerSerializer(serializers.ModelSerializer):
    """Customer serializer."""
    phone_regex = RegexValidator(regex=r'^\d{10,14}$',
                                 message="Phone number must be between 10 to 14 digits.")
    phone_number = serializers.CharField(max_length=18, validators=[phone_regex])

    class Meta:
        model = Customer
        exclude = ('created_at', 'updated_at')

    def validate_email(self, value):
        # validate customer does not exist
        if (self.context["request"].method == "POST") and (Customer.objects.filter(email=value).exists()):
            raise serializers.ValidationError("Customer already added.")
        return value


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer."""

    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Payment
        exclude = ('created_at', 'updated_at')

    def __init__(self, customer, *args, **kwargs):
        self.customer = customer
        return super().__init__(*args, **kwargs)

    def validate(self, data):
        verified = data.get("verified")
        if verified is not None and verified is False:
            raise serializers.ValidationError("Please verify payment before submitting")
        if verified is None:
            raise serializers.ValidationError({"verified": ["Verification is required"]})
        return data
