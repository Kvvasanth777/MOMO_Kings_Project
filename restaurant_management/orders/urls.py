from django.urls import path
from .views import GetCartAjaxView, AddToCartAjaxView, UpdateCartAjaxView, ApplyCouponAjaxView, CheckoutView, TrackOrderView

urlpatterns = [
    path('cart/', GetCartAjaxView.as_view(), name='get_cart_ajax'),
    path('cart/add/', AddToCartAjaxView.as_view(), name='add_to_cart_ajax'),
    path('cart/update/', UpdateCartAjaxView.as_view(), name='update_cart_ajax'),
    path('coupon/apply/', ApplyCouponAjaxView.as_view(), name='apply_coupon_ajax'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('track/<int:order_id>/', TrackOrderView.as_view(), name='track_order'),
]
