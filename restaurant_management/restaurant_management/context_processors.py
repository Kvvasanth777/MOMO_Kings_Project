def global_context(request):
    context = {}

    # 1. Fetch Categories for Navigation
    try:
        from menu.models import Category
        context['nav_categories'] = Category.objects.filter(is_active=True)[:6]
    except Exception:
        context['nav_categories'] = []

    # 2. Cart count
    cart_count = 0
    if request.user.is_authenticated:
        try:
            from orders.models import Cart
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_count = sum(item.quantity for item in cart.items.all())
        except Exception:
            pass
    else:
        session_cart = request.session.get('cart', {})
        cart_count = sum(item.get('quantity', 0) for item in session_cart.values())

    context['global_cart_count'] = cart_count

    # 3. Unread Notifications
    if request.user.is_authenticated:
        try:
            from orders.models import Notification
            context['global_notifications'] = Notification.objects.filter(
                user=request.user, is_read=False
            ).order_by('-created_at')[:5]
        except Exception:
            context['global_notifications'] = []
    else:
        context['global_notifications'] = []

    return context
