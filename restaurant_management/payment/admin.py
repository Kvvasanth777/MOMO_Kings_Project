from django.contrib import admin
from .models import Payment, Invoice

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id', 'order', 'amount', 'method', 'status', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['payment_id', 'order__id']

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'order', 'created_at']
    search_fields = ['invoice_number', 'order__id']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Invoice, InvoiceAdmin)
