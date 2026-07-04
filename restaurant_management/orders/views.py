from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from menu.models import FoodItem
from .models import Cart, CartItem, Order, OrderItem, Coupon, Notification


class GetCartAjaxView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse(
                {'success': False, 'message': 'Login required'}, status=401
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        items_data = []
        for item in cart.items.select_related('food_item').all():
            if item.food_item.image:
                img_url = item.food_item.image.url
            elif item.food_item.image_url:
                img_url = item.food_item.image_url
            else:
                img_url = '/static/images/default-food.jpg'

            items_data.append({
                'id': item.id,
                'food_id': item.food_item.id,
                'name': item.food_item.name,
                'price': str(item.food_item.price),
                'quantity': item.quantity,
                'image_url': img_url,
                'total_price': str(item.get_total_price()),
            })

        subtotal = cart.get_subtotal()

        # Check session coupon
        coupon_code = request.session.get('coupon_code', None)
        discount_percent = 0
        discount_amount = Decimal('0.00')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(
                    code=coupon_code, active=True, expiry__gte=timezone.now().date()
                )
                discount_percent = coupon.discount_percent
                discount_amount = (subtotal * Decimal(discount_percent)) / 100
            except Coupon.DoesNotExist:
                pass

        packing_charge = Decimal('30.00') if subtotal > 0 else Decimal('0.00')
        gst = subtotal * Decimal('0.05')
        grand_total = max(Decimal('0.00'), subtotal + packing_charge + gst - discount_amount)

        return JsonResponse({
            'success': True,
            'items': items_data,
            'subtotal': str(subtotal),
            'discount_percent': discount_percent,
            'discount_amount': str(discount_amount),
            'packing_charge': str(packing_charge),
            'gst': str(gst),
            'grand_total': str(grand_total),
        })


class AddToCartAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        food_id = request.POST.get('food_id')
        quantity = int(request.POST.get('quantity', 1))
        food_item = get_object_or_404(FoodItem, id=food_id, is_active=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, food_item=food_item
        )

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        cart_count = sum(i.quantity for i in cart.items.all())
        return JsonResponse({
            'success': True,
            'message': f"Added {food_item.name} to cart",
            'cart_count': cart_count,
        })


class UpdateCartAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            cart_item.quantity -= 1
            if cart_item.quantity <= 0:
                cart_item.delete()
            else:
                cart_item.save()
        elif action == 'remove':
            cart_item.delete()

        try:
            cart = Cart.objects.get(user=request.user)
            cart_count = sum(i.quantity for i in cart.items.all())
        except Cart.DoesNotExist:
            cart_count = 0

        return JsonResponse({'success': True, 'cart_count': cart_count})


class ApplyCouponAjaxView(LoginRequiredMixin, View):
    def post(self, request):
        code = request.POST.get('code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(
                code=code, active=True, expiry__gte=timezone.now().date()
            )
            request.session['coupon_code'] = coupon.code
            return JsonResponse({
                'success': True,
                'message': f"Coupon '{code}' applied! {coupon.discount_percent}% discount."
            })
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': "Invalid or expired coupon."})


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return redirect('menu_list')

        subtotal = cart.get_subtotal()
        coupon_code = request.session.get('coupon_code', None)
        discount_amount = Decimal('0.00')
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                discount_amount = (subtotal * Decimal(coupon.discount_percent)) / 100
            except Coupon.DoesNotExist:
                pass

        packing_charge = Decimal('30.00')
        gst = subtotal * Decimal('0.05')
        grand_total = subtotal + packing_charge + gst - discount_amount

        context = {
            'cart': cart,
            'subtotal': subtotal,
            'discount': discount_amount,
            'packing_charge': packing_charge,
            'gst': gst,
            'grand_total': grand_total,
            'coupon': coupon,
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return redirect('menu_list')

        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        delivery_type = request.POST.get('delivery_type', 'Delivery')
        table_number = request.POST.get('table_number', '')
        address = request.POST.get('address', '')
        notes = request.POST.get('notes', '')

        subtotal = cart.get_subtotal()
        coupon_code = request.session.get('coupon_code', None)
        discount_amount = Decimal('0.00')
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True)
                discount_amount = (subtotal * Decimal(coupon.discount_percent)) / 100
            except Coupon.DoesNotExist:
                pass

        packing_charge = Decimal('30.00')
        gst = subtotal * Decimal('0.05')
        grand_total = subtotal + packing_charge + gst - discount_amount

        order = Order.objects.create(
            user=request.user,
            customer_name=name,
            phone_number=phone,
            email=email,
            delivery_type=delivery_type,
            table_number=table_number if delivery_type == 'Dining' else None,
            address=address if delivery_type == 'Delivery' else None,
            notes=notes,
            subtotal=subtotal,
            packing_charge=packing_charge,
            gst=gst,
            discount=discount_amount,
            grand_total=grand_total,
            coupon_applied=coupon,
            status='Pending',
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_item=item.food_item,
                quantity=item.quantity,
                price=item.food_item.price,
            )

        cart.items.all().delete()
        if 'coupon_code' in request.session:
            del request.session['coupon_code']

        Notification.objects.create(
            user=request.user,
            message=f"Order #{order.id} placed! Mode: {delivery_type}. Total: Rs.{grand_total:.2f}"
        )

        return redirect('process_payment', order_id=order.id)


class TrackOrderView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        status_flow = [
            'Pending', 'Confirmed', 'Preparing', 'Ready',
            'Out For Delivery', 'Delivered', 'Completed'
        ]
        status_index = 0
        if order.status in status_flow:
            status_index = status_flow.index(order.status)

        progress_percent = int((status_index / (len(status_flow) - 1)) * 100)

        context = {
            'order': order,
            'status_flow': status_flow,
            'status_index': status_index,
            'progress_percent': progress_percent,
        }
        return render(request, 'track_order.html', context)
