import io
import qrcode

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Category, FoodItem, Review, Wishlist


class LandingPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)[:6]
        context['chef_specials'] = FoodItem.objects.filter(
            is_chef_special=True, is_active=True
        )[:4]
        context['popular_items'] = FoodItem.objects.filter(
            is_popular=True, is_active=True
        )[:4]
        context['recent_reviews'] = Review.objects.all().order_by('-created_at')[:4]
        return context


class MenuListView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        category_slug = request.GET.get('category', '')
        sort_by = request.GET.get('sort', '')
        veg_filter = request.GET.get('veg', '')

        items = FoodItem.objects.filter(is_active=True)

        if query:
            items = items.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        if category_slug:
            items = items.filter(category__slug=category_slug)
        if veg_filter:
            items = items.filter(veg_non_veg=veg_filter)
        if sort_by == 'price_asc':
            items = items.order_by('price')
        elif sort_by == 'price_desc':
            items = items.order_by('-price')
        elif sort_by == 'rating':
            items = items.order_by('-rating')
        elif sort_by == 'calories':
            items = items.order_by('calories')

        # Wishlist item ids for current user
        wishlist_item_ids = []
        if request.user.is_authenticated:
            try:
                wishlist = Wishlist.objects.get(user=request.user)
                wishlist_item_ids = list(wishlist.items.values_list('id', flat=True))
            except Wishlist.DoesNotExist:
                pass

        categories = Category.objects.filter(is_active=True)
        context = {
            'items': items,
            'categories': categories,
            'selected_category': category_slug,
            'query': query,
            'sort_by': sort_by,
            'veg_filter': veg_filter,
            'wishlist_item_ids': wishlist_item_ids,
        }
        return render(request, 'menu.html', context)


class FoodItemDetailAjaxView(View):
    def get(self, request, pk):
        item = get_object_or_404(FoodItem, pk=pk)
        if item.image:
            image_url = item.image.url
        elif item.image_url:
            image_url = item.image_url
        else:
            image_url = '/static/images/default-food.jpg'

        data = {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': str(item.price),
            'image_url': image_url,
            'veg_non_veg': item.veg_non_veg,
            'rating': float(item.rating),
            'prep_time': item.prep_time,
            'calories': item.calories,
            'spice_level': item.spice_level,
        }
        return JsonResponse(data)


class ToggleWishlistAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        item = get_object_or_404(FoodItem, id=item_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        if item in wishlist.items.all():
            wishlist.items.remove(item)
            added = False
            message = "Removed from wishlist"
        else:
            wishlist.items.add(item)
            added = True
            message = "Added to wishlist"

        return JsonResponse({'success': True, 'added': added, 'message': message})


class GenerateQRCodeView(View):
    def get(self, request):
        menu_url = request.build_absolute_uri('/menu/')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(menu_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
