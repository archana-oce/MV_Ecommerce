from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    # We add this so React can show the Shop Name without a second API call
    vendor_name = serializers.ReadOnlyField(source='vendor.business_name')

    class Meta:
        model = Product
        fields = [
            'id', 'vendor', 'vendor_name', 'name', 
            'description', 'price', 'stock', 'image', 'created_at'
        ]