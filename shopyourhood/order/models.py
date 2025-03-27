from django.utils import timezone
from django.db import models
from django.conf import settings
from products.models import Product
from authentication.models import ShopProfile

class Booking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    

    def start_timer(self):
        self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        self.save()

    def is_active(self):
        return self.status == 'approved' and self.expires_at > timezone.now()

class CartItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class OrderRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    shop_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def approve(self):
        self.status = 'approved'
        self.booking.start_timer()
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()
