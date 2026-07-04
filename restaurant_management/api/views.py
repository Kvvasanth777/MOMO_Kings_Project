from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from accounts.models import User
from menu.models import Category, FoodItem, Review, Wishlist
from orders.models import Cart, CartItem, Order
from payment.models import Payment
from .serializers import (
    UserSerializer, CategorySerializer, FoodItemSerializer,
    ReviewSerializer, CartSerializer, OrderSerializer, PaymentSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class FoodItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FoodItem.objects.filter(is_active=True)
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        food_id = request.data.get('food_id')
        qty = int(request.data.get('quantity', 1))
        
        try:
            food_item = FoodItem.objects.get(id=food_id, is_active=True)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
            if not item_created:
                cart_item.quantity += qty
            else:
                cart_item.quantity = qty
            cart_item.save()
            return Response({'status': 'Item added to cart'}, status=status.HTTP_200_OK)
        except FoodItem.DoesNotExist:
            return Response({'error': 'Food item not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(order__user=self.request.user)
