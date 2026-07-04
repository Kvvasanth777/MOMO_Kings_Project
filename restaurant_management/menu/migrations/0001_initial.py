from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=120, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('image', models.ImageField(blank=True, null=True, upload_to='menu_items/')),
                ('image_url', models.URLField(blank=True, max_length=500, null=True)),
                ('spice_level', models.IntegerField(default=0)),
                ('prep_time', models.IntegerField(default=15)),
                ('calories', models.IntegerField(default=300)),
                ('rating', models.DecimalField(decimal_places=1, default=4.5, max_digits=3)),
                ('veg_non_veg', models.CharField(
                    choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')],
                    default='Veg', max_length=10
                )),
                ('is_popular', models.BooleanField(default=False)),
                ('is_chef_special', models.BooleanField(default=False)),
                ('is_recommended', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='food_items',
                    to='menu.category'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=5)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('food_item', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reviews',
                    to='menu.fooditem'
                )),
                ('user', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='accounts.user'
                )),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('items', models.ManyToManyField(blank=True, to='menu.fooditem')),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='wishlist',
                    to='accounts.user'
                )),
            ],
        ),
    ]
