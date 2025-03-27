from django.contrib.auth.models import AbstractUser
from django.db import models

# CustomUser model with user type
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'customer'),
        (2, 'shop_owner'),
        (3, 'admin'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

# Customer Profile Model
class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    remember_me = models.BooleanField(default=False)

# Shop Owner Profile Model
class ShopProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    owner_name = models.CharField(max_length=255)
    shop_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)  # For district or later latitude/longitude
    shop_proof = models.ImageField(upload_to='shop_proofs/')  # Image upload for shop proof
    is_verified = models.BooleanField(default=False)

