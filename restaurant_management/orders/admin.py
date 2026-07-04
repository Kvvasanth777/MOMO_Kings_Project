from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Coupon, Notification

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'delivery_type', 'grand_total', 'status', 'created_at']
    list_filter = ['status', 'delivery_type', 'created_at']
    search_fields = ['customer_name', 'phone_number', 'email']
    inlines = [OrderItemInline]

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Coupon)
admin.site.register(Notification)
