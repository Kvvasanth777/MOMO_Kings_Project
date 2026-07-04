from django.test import TestCase
from django.contrib.auth import get_user_model
from menu.models import Category, FoodItem
from orders.models import Cart, CartItem, Order, Coupon
from decimal import Decimal
import datetime

User = get_user_model()

class MomoKingsTestCase(TestCase):
    def setUp(self):
        # 1. Create User
        self.user = User.objects.create_user(username='royal_guest', password='guestpassword123')
        
        # 2. Create Category and FoodItems
        self.category = Category.objects.create(name='Imperial Dumplings', slug='imperial-dumplings')
        self.food_item = FoodItem.objects.create(
            name='Truffle Momo',
            slug='truffle-momo',
            description='Premium truffle dumplings.',
            price=Decimal('300.00'),
            category=self.category
        )
        
        # 3. Create Coupon
        self.coupon = Coupon.objects.create(
            code='ROYALTEST',
            discount_percent=10,
            active=True,
            expiry=datetime.date(2030, 12, 31)
        )

    def test_cart_operations(self):
        # Verify cart auto-created or fetched
        cart, created = Cart.objects.get_or_create(user=self.user)
        self.assertEqual(cart.items.count(), 0)

        # Add item to cart
        cart_item = CartItem.objects.create(cart=cart, food_item=self.food_item, quantity=2)
        self.assertEqual(cart.get_subtotal(), Decimal('600.00'))
        self.assertEqual(cart_item.get_total_price(), Decimal('600.00'))

    def test_order_creation_with_totals(self):
        # Place test Order
        subtotal = Decimal('600.00')
        packing_charge = Decimal('30.00')
        gst = subtotal * Decimal('0.05') # 5% GST -> 30.00
        discount = (subtotal * Decimal('10')) / 100 # 10% coupon -> 60.00
        grand_total = subtotal + packing_charge + gst - discount # 600 + 30 + 30 - 60 = 600.00

        order = Order.objects.create(
            user=self.user,
            customer_name='Royal Guest',
            phone_number='9876543210',
            email='guest@royal.com',
            delivery_type='Delivery',
            subtotal=subtotal,
            packing_charge=packing_charge,
            gst=gst,
            discount=discount,
            grand_total=grand_total,
            coupon_applied=self.coupon,
            status='Pending'
        )

        self.assertEqual(order.grand_total, Decimal('600.00'))
        self.assertEqual(order.status, 'Pending')
