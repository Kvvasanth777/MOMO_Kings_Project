from django.contrib import admin
from .models import Category, FoodItem, Review, Wishlist

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'veg_non_veg', 'rating', 'is_active']
    list_filter = ['category', 'veg_non_veg', 'is_active', 'is_popular', 'is_chef_special']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(Review)
admin.site.register(Wishlist)
