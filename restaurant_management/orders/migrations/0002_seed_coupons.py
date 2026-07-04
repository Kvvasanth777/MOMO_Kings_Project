from django.db import migrations
import datetime

def seed_coupons(apps, schema_editor):
    Coupon = apps.get_model('orders', 'Coupon')
    
    # Create Coupons
    Coupon.objects.create(
        code='ROYAL10',
        discount_percent=10,
        active=True,
        expiry=datetime.date(2030, 12, 31)
    )
    Coupon.objects.create(
        code='MOMOKINGS20',
        discount_percent=20,
        active=True,
        expiry=datetime.date(2030, 12, 31)
    )

def remove_coupons(apps, schema_editor):
    Coupon = apps.get_model('orders', 'Coupon')
    Coupon.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_coupons, remove_coupons),
    ]
