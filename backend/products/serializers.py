from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.business_name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'category', 'vendor', 'vendor_name', 'color', 
            'weight', 'average_rating', 'update_history', 'created_at'
        ]