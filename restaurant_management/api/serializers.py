from rest_framework import serializers
from accounts.models import User, CustomerProfile
from menu.models import Category, FoodItem, Review, Wishlist
from orders.models import Cart, CartItem, Order, OrderItem, Coupon
from payment.models import Payment, Invoice

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'loyalty_points', 'referral_code']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image_url', 'is_active']

class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = FoodItem
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'image_url', 
            'category', 'category_name', 'spice_level', 'prep_time', 
            'calories', 'rating', 'veg_non_veg', 'is_popular', 
            'is_chef_special', 'is_recommended', 'is_active'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'food_item', 'username', 'rating', 'comment', 'created_at']

class WishlistSerializer(serializers.ModelSerializer):
    items = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'items']

class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(), write_only=True, source='food_item'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'food_item', 'food_item_id', 'quantity', 'get_total_price']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'subtotal']

    def get_subtotal(self, obj):
        return str(obj.get_subtotal())

class OrderItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.ReadOnlyField(source='food_item.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'food_item_name', 'quantity', 'price', 'get_total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'customer_name', 'phone_number', 'email', 
            'delivery_type', 'table_number', 'address', 'notes', 
            'subtotal', 'packing_charge', 'gst', 'discount', 
            'grand_total', 'status', 'items', 'created_at'
        ]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_id', 'amount', 'status', 'method', 'created_at']
