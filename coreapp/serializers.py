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
        if len(value) != 12:
            raise serializers.ValidationError("Phone number must be 10 digits long.")


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = '__all__'
