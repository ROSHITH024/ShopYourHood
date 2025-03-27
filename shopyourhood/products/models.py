from django.db import models
from authentication.models import ShopProfile

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('home', 'Home & Kitchen'),
        ('books', 'Books'),
        ('toys', 'Toys & Games'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    is_verified = models.BooleanField(default=False)
    added_by = models.ForeignKey(ShopProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class ShopProduct(models.Model):
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['shop', 'product']  # Ensure each shop can only add a product once
