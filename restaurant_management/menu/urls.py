from django.urls import path
from .views import MenuListView, FoodItemDetailAjaxView, ToggleWishlistAjaxView, GenerateQRCodeView

urlpatterns = [
    path('', MenuListView.as_view(), name='menu_list'),
    path('item/<int:pk>/', FoodItemDetailAjaxView.as_view(), name='food_detail_ajax'),
    path('wishlist/toggle/', ToggleWishlistAjaxView.as_view(), name='toggle_wishlist_ajax'),
    path('qrcode/', GenerateQRCodeView.as_view(), name='generate_qrcode'),
]
