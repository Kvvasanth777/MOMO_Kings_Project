from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount_percent', models.IntegerField(default=10)),
                ('active', models.BooleanField(default=True)),
                ('expiry', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='cart',
                    to='accounts.user'
                )),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='orders.cart'
                )),
                ('food_item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='menu.fooditem'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='notifications',
                    to='accounts.user'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('delivery_type', models.CharField(
                    choices=[('Delivery', 'Delivery'), ('Takeaway', 'Takeaway'), ('Dining', 'Dining')],
                    default='Delivery', max_length=20
                )),
                ('table_number', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10)),
                ('packing_charge', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('gst', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(
                    choices=[
                        ('Pending', 'Pending'), ('Confirmed', 'Confirmed'),
                        ('Preparing', 'Preparing'), ('Ready', 'Ready'),
                        ('Out For Delivery', 'Out For Delivery'), ('Delivered', 'Delivered'),
                        ('Completed', 'Completed'), ('Cancelled', 'Cancelled'),
                    ],
                    default='Pending', max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coupon_applied', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='orders.coupon'
                )),
                ('user', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='accounts.user'
                )),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('food_item', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='menu.fooditem'
                )),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='items',
                    to='orders.order'
                )),
            ],
        ),
    ]
