from rest_framework import serializers
from .models import User, Vendor
from rest_framework import permissions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','role'] 
        read_only_fields = ['role']
class VendorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # Nested serializer to show user details
    
    class Meta:
        model = Vendor
        fields = ['id', 'user', 'phone', 'business_name', 'company_name', 'is_approved']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        # 2. Add your custom "Role-Based" data
        token['role'] = user.role
        token['email'] = user.email
        token['username'] = user.username

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        
       
        if self.user.role == 'vendor':
            try:
                data['is_approved'] = self.user.vendor_profile.is_approved
            except Vendor.DoesNotExist:
                
                data['is_approved'] = False
                
        return data
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password'] # Removed 'role' from fields

    def create(self, validated_data):
        # Every person signing up through the website is automatically a Customer
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role='customer' # Hardcoded safety
        )
        return user
    