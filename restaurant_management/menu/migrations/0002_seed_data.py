from django.db import migrations


def seed_menu_data(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    FoodItem = apps.get_model('menu', 'FoodItem')

    # --- Categories ---
    combos = Category.objects.create(
        name='Combo Meals', slug='combo-meals',
        description='Royal combos with premium sides.',
        image_url='https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=600&auto=format&fit=crop'
    )
    momos = Category.objects.create(
        name='Momos', slug='momos',
        description='Hand-wrapped royal Himalayan dumplings.',
        image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?q=80&w=600&auto=format&fit=crop'
    )
    soups = Category.objects.create(
        name='Soups', slug='soups',
        description='Delicate broths and signature stocks.',
        image_url='https://images.unsplash.com/photo-1547928712-780c21384003?q=80&w=600&auto=format&fit=crop'
    )
    starters = Category.objects.create(
        name='Starters', slug='starters',
        description='Mouth-watering appetisers.',
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )
    noodles = Category.objects.create(
        name='Noodles', slug='noodles',
        description='Wok-tossed imperial wheat strands.',
        image_url='https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=600&auto=format&fit=crop'
    )
    fried_rice = Category.objects.create(
        name='Fried Rice', slug='fried-rice',
        description='Premium wok-tossed rice dishes.',
        image_url='https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=600&auto=format&fit=crop'
    )
    chop_suey = Category.objects.create(
        name='Chop Suey', slug='chop-suey',
        description='Crispy noodle specialties.',
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )
    milkshakes = Category.objects.create(
        name='Milkshakes', slug='milkshakes',
        description='Rich, creamy imperial milkshakes.',
        image_url='https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=600&auto=format&fit=crop'
    )
    mojitos = Category.objects.create(
        name='Mojitos', slug='mojitos',
        description='Sparkling refreshing elixirs.',
        image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=600&auto=format&fit=crop'
    )

    # --- Food Items ---
    # MOMOS
    FoodItem.objects.create(
        name='Gold Saffron Momo', slug='gold-saffron-momo',
        description='Hand-wrapped saffron dough with spiced paneer filling and gold leaf.',
        price=399, category=momos, spice_level=1, prep_time=15, calories=280, rating=4.9,
        veg_non_veg='Veg', is_chef_special=True, is_popular=True,
        image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Royal Chicken Jhol Momo', slug='royal-chicken-jhol-momo',
        description='Savory chicken dumplings in spiced sesame-tomato soup broth.',
        price=429, category=momos, spice_level=2, prep_time=20, calories=320, rating=4.8,
        veg_non_veg='Non-Veg', is_recommended=True, is_popular=True,
        image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Truffle Cheese Steam Momo', slug='truffle-cheese-steam-momo',
        description='Gourmet steamed momos with black truffle oil and creamy cheddar.',
        price=459, category=momos, spice_level=0, prep_time=15, calories=290, rating=4.7,
        veg_non_veg='Veg', is_popular=True,
        image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Spicy Tandoor Momo', slug='spicy-tandoor-momo',
        description='Char-grilled momos with smoky tandoor seasoning and mint chutney.',
        price=379, category=momos, spice_level=3, prep_time=18, calories=310, rating=4.6,
        veg_non_veg='Non-Veg',
        image_url='https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?q=80&w=600&auto=format&fit=crop'
    )

    # SOUPS
    FoodItem.objects.create(
        name='Imperial Tom Yum Soup', slug='imperial-tom-yum',
        description='Hot and sour clear soup with lemongrass, kaffir lime, and galangal.',
        price=289, category=soups, spice_level=2, prep_time=12, calories=150, rating=4.5,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1547928712-780c21384003?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Royal Thukpa Broth', slug='royal-thukpa-broth',
        description='Traditional Himalayan noodle soup with fresh vegetables and warming spices.',
        price=319, category=soups, spice_level=1, prep_time=15, calories=210, rating=4.6,
        veg_non_veg='Non-Veg', is_recommended=True,
        image_url='https://images.unsplash.com/photo-1547928712-780c21384003?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Sweet Corn Soup', slug='sweet-corn-soup',
        description='Silky sweet corn and vegetable soup with black pepper and ginger.',
        price=249, category=soups, spice_level=0, prep_time=10, calories=180, rating=4.4,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1547928712-780c21384003?q=80&w=600&auto=format&fit=crop'
    )

    # NOODLES
    FoodItem.objects.create(
        name='Wok-Fried Garlic Hakka Noodles', slug='garlic-hakka-noodles',
        description='Wok-tossed noodles with organic vegetables, burnt garlic, and premium soy sauce.',
        price=349, category=noodles, spice_level=1, prep_time=18, calories=420, rating=4.6,
        veg_non_veg='Veg', is_recommended=True,
        image_url='https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Sichuan Pepper Chicken Noodles', slug='sichuan-pepper-noodles',
        description='Fiery noodles with chicken breast, scallions, and Sichuan pepper corn oil.',
        price=399, category=noodles, spice_level=3, prep_time=18, calories=490, rating=4.7,
        veg_non_veg='Non-Veg', is_chef_special=True,
        image_url='https://images.unsplash.com/photo-1585032226651-759b368d7246?q=80&w=600&auto=format&fit=crop'
    )

    # FRIED RICE
    FoodItem.objects.create(
        name='Imperial Egg Fried Rice', slug='imperial-egg-fried-rice',
        description='Wok-tossed jasmine rice with farm eggs, spring onions, and sesame oil.',
        price=329, category=fried_rice, spice_level=1, prep_time=15, calories=450, rating=4.5,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Royal Chicken Fried Rice', slug='royal-chicken-fried-rice',
        description='Fragrant rice tossed with spiced chicken, carrots, peas, and dark soy.',
        price=379, category=fried_rice, spice_level=2, prep_time=18, calories=520, rating=4.7,
        veg_non_veg='Non-Veg', is_popular=True,
        image_url='https://images.unsplash.com/photo-1512058564366-18510be2db19?q=80&w=600&auto=format&fit=crop'
    )

    # STARTERS
    FoodItem.objects.create(
        name='Crispy Corn Starters', slug='crispy-corn-starters',
        description='Golden fried sweet corn kernels with chilli flakes and lime dressing.',
        price=269, category=starters, spice_level=2, prep_time=12, calories=310, rating=4.5,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Chilli Paneer Dry', slug='chilli-paneer-dry',
        description='Crispy paneer cubes tossed with bell peppers in a tangy Indo-Chinese sauce.',
        price=349, category=starters, spice_level=2, prep_time=15, calories=380, rating=4.7,
        veg_non_veg='Veg', is_popular=True,
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )

    # CHOP SUEY
    FoodItem.objects.create(
        name='Royal Crispy Chop Suey', slug='royal-crispy-chop-suey',
        description='Crispy noodles topped with wok vegetables and sweet-sour chicken sauce.',
        price=489, category=chop_suey, spice_level=1, prep_time=20, calories=540, rating=4.8,
        veg_non_veg='Non-Veg', is_chef_special=True,
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Veg Chop Suey', slug='veg-chop-suey',
        description='Crispy noodles with seasonal vegetables in a garlic oyster sauce.',
        price=429, category=chop_suey, spice_level=1, prep_time=20, calories=480, rating=4.5,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600&auto=format&fit=crop'
    )

    # MILKSHAKES
    FoodItem.objects.create(
        name='Royal Belgian Chocolate Shake', slug='royal-belgian-chocolate-shake',
        description='Rich imported Belgian dark chocolate blended with premium ice cream.',
        price=299, category=milkshakes, spice_level=0, prep_time=8, calories=480, rating=4.8,
        veg_non_veg='Veg', is_popular=True,
        image_url='https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Himalayan Strawberry Shake', slug='himalayan-strawberry-shake',
        description='Fresh strawberries blended with organic milk and rose water.',
        price=269, category=milkshakes, spice_level=0, prep_time=8, calories=380, rating=4.6,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1572490122747-3968b75cc699?q=80&w=600&auto=format&fit=crop'
    )

    # MOJITOS
    FoodItem.objects.create(
        name='Elite Himalayan Mint Mojito', slug='himalayan-mint-mojito',
        description='Fresh mountain mint, crushed lime, and pure organic cane sparkling water.',
        price=249, category=mojitos, spice_level=0, prep_time=8, calories=120, rating=4.7,
        veg_non_veg='Veg', is_recommended=True,
        image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Royal Watermelon Bliss Mojito', slug='royal-watermelon-mojito',
        description='Fresh watermelon, fresh mint, lime juice, and chilled soda water.',
        price=229, category=mojitos, spice_level=0, prep_time=6, calories=100, rating=4.5,
        veg_non_veg='Veg',
        image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=600&auto=format&fit=crop'
    )

    # COMBOS
    FoodItem.objects.create(
        name='Royal Momo Meal Combo', slug='royal-momo-meal-combo',
        description='8 pcs steamed momos + soup + fried rice + mocktail. Perfect royal meal.',
        price=699, category=combos, spice_level=1, prep_time=25, calories=820, rating=4.9,
        veg_non_veg='Veg', is_popular=True, is_chef_special=True, is_recommended=True,
        image_url='https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=600&auto=format&fit=crop'
    )
    FoodItem.objects.create(
        name='Non-Veg Feast Combo', slug='non-veg-feast-combo',
        description='6 chicken momos + thukpa + chicken fried rice + special mojito.',
        price=799, category=combos, spice_level=2, prep_time=30, calories=950, rating=4.8,
        veg_non_veg='Non-Veg', is_popular=True, is_chef_special=True,
        image_url='https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=600&auto=format&fit=crop'
    )


def remove_menu_data(apps, schema_editor):
    FoodItem = apps.get_model('menu', 'FoodItem')
    Category = apps.get_model('menu', 'Category')
    FoodItem.objects.all().delete()
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_menu_data, remove_menu_data),
    ]
