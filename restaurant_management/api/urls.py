from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, FoodItemViewSet, 
    ReviewViewSet, CartViewSet, OrderViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='api-users')
router.register('categories', CategoryViewSet, basename='api-categories')
router.register('menu', FoodItemViewSet, basename='api-menu')
router.register('reviews', ReviewViewSet, basename='api-reviews')
router.register('cart', CartViewSet, basename='api-cart')
router.register('orders', OrderViewSet, basename='api-orders')
router.register('payments', PaymentViewSet, basename='api-payments')

urlpatterns = [
    path('', include(router.urls)),
]
