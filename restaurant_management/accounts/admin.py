from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'phone_number', 'loyalty_points', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'avatar', 'loyalty_points', 'referral_code')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'phone_number', 'avatar', 'loyalty_points', 'referral_code')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(CustomerProfile)
