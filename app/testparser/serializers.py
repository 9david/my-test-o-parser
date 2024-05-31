"""
Serializers for product API.
"""
from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.Serializer):
    """Serializer for products."""
    name = serializers.CharField(max_length=255)
    price = serializers.IntegerField()
    description = serializers.CharField(max_length=255)
    image_url = serializers.URLField(max_length=255)
    discount = serializers.CharField(max_length=255)

class ProductPostSerializer(serializers.Serializer):
    """Serializer for custom post method"""
    products_count = serializers.IntegerField(min_value=0, max_value=50)

