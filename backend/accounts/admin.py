from django.contrib import admin
from .models import User, Vendor
from django.contrib import admin

class VendorInline(admin.StackedInline):
    model = Vendor
    can_delete = False
    verbose_name_plural = 'Vendor Profile'

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (VendorInline,)
    list_display = ('email', 'username', 'role', 'is_active')
    list_filter = ('role', 'is_active')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Vendor)