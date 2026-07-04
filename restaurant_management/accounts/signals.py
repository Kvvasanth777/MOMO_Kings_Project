from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile_elements(sender, instance, created, **kwargs):
    if created:
        from .models import CustomerProfile
        from menu.models import Wishlist
        from orders.models import Cart
        CustomerProfile.objects.get_or_create(user=instance)
        Wishlist.objects.get_or_create(user=instance)
        Cart.objects.get_or_create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile_elements(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        try:
            instance.profile.save()
        except Exception:
            pass
    if hasattr(instance, 'wishlist'):
        try:
            instance.wishlist.save()
        except Exception:
            pass
    if hasattr(instance, 'cart'):
        try:
            instance.cart.save()
        except Exception:
            pass
