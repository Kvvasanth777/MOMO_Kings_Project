from django.db import models
from orders.models import Order
import uuid

class Payment(models.Model):
    METHOD_CHOICES = [
        ('Razorpay', 'Razorpay'),
        ('UPI', 'UPI'),
        ('COD', 'Cash On Delivery'),
        ('Card', 'Credit/Debit Card'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending') # Pending, Success, Failed
    method = models.CharField(max_length=20, choices=METHOD_CHOICES, default='Razorpay')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Order #{self.order.id}"

class Invoice(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = f"INV-{uuid.uuid4().hex[:10].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} for Order #{self.order.id}"
