from rest_framework import serializers
from .models import User, Vendor

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested serializer to show user details
    
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'phone', 'business_name', 'company_name', 'is_approved']