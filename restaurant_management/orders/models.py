from django.db import models
from django.conf import settings
from menu.models import FoodItem

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_subtotal(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_total_price(self):
        return self.food_item.price * self.quantity

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount_percent = models.IntegerField(default=10)
    active = models.BooleanField(default=True)
    expiry = models.DateField()

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    DELIVERY_CHOICES = [
        ('Delivery', 'Delivery'),
        ('Takeaway', 'Takeaway'),
        ('Dining', 'Dining'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='Delivery')
    table_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    packing_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    gst = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    coupon_applied = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name if self.food_item else 'Unknown Item'}"

    def get_total_price(self):
        return self.price * self.quantity

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:30]}"
