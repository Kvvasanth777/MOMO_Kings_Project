from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class FoodItem(models.Model):
    VEG_CHOICES = [
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='food_items')
    spice_level = models.IntegerField(default=0) # 0 to 3
    prep_time = models.IntegerField(default=15) # minutes
    calories = models.IntegerField(default=300)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    veg_non_veg = models.CharField(max_length=10, choices=VEG_CHOICES, default='Veg')
    is_popular = models.BooleanField(default=False)
    is_chef_special = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.food_item.name}"

class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    items = models.ManyToManyField(FoodItem, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
