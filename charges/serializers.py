from rest_framework import serializers
from .models import Seller, Costumer


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'username', 'credit']


class CostumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costumer
        fields = ['id', 'phone_number', 'credit']


class SellRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=25, decimal_places=10)


class SellerIncreaseSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=25, decimal_places=10)


class DeleteSellerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)


class DeleteCostumerSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=100)
