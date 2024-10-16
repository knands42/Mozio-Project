from rest_framework import serializers
from .models import Provider, ServiceArea

def validate_currency(value):
    valid_currencies = ['USD', 'EUR']
    if value not in valid_currencies:
        raise serializers.ValidationError(f"Currency must be one of {valid_currencies}.")


class ProviderSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(validators=[validate_currency])
    
    class Meta:
        model = Provider
        fields = '__all__'

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        
        return value


class ServiceAreaSerializer(serializers.ModelSerializer):
    def validate_area(self, value):
        """
        Validate that the input consists of at least three coordinate points to form a valid polygon.
        """
        if len(value) < 3:
            raise serializers.ValidationError("A valid polygon must have at least three coordinates.")
        return value

    
    class Meta:
        model = ServiceArea
        fields = '__all__'
