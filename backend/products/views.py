from rest_framework import generics, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer
from rest_framework import permissions

class IsApprovedVendor(permissions.BasePermission):
    """
    Allow only users who are Vendors AND have been approved by Archana (Admin).
    """
    def has_permission(self, request, view):
        # Safe methods like GET, HEAD, OPTIONS are allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # For POST (Create), check if user is a vendor and approved
        return (
            request.user.is_authenticated and 
            request.user.role == 'vendor' and 
            hasattr(request.user, 'vendor_profile') and
            request.user.vendor_profile.is_approved
        )
    
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    # Use our custom permission here
    permission_classes = [IsApprovedVendor]

    def perform_create(self, serializer):
        # This link connects the product to the vendor automatically
        # so the Vendor doesn't have to manually select their own name in React.
        serializer.save(vendor=self.request.user.vendor_profile)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles Viewing a single product, Updating it, or Deleting it.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsApprovedVendor]

    def get_queryset(self):
       
        #  Vendors can only Update/Delete THEIR OWN products.
        if self.request.method in permissions.SAFE_METHODS:
            return Product.objects.all()
        return Product.objects.filter(vendor=self.request.user.vendor_profile)