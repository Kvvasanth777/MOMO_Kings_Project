from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('method', models.CharField(
                    choices=[
                        ('Razorpay', 'Razorpay'), ('UPI', 'UPI'),
                        ('COD', 'Cash On Delivery'), ('Card', 'Credit/Debit Card'),
                    ],
                    default='Razorpay', max_length=20
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='payments',
                    to='orders.order'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='invoice',
                    to='orders.order'
                )),
            ],
        ),
    ]
