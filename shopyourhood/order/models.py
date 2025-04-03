from django.utils import timezone
from django.db import models
from django.conf import settings
from products.models import Product, ShopProduct
from authentication.models import ShopProfile
from django.utils.timezone import now

class Booking(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ Add price field
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def start_timer(self):
        self.expires_at = timezone.now() + timezone.timedelta(hours=24)
        self.save()

    def is_active(self):
        return self.status == 'approved' and (self.expires_at is None or self.expires_at > timezone.now())

    def save(self, *args, **kwargs):
        """ Automatically set price based on ShopProduct """
        if not self.price:  # Only set price if it's not already provided
            shop_product = ShopProduct.objects.filter(shop=self.shop, product=self.product).first()
            if shop_product:
                self.price = shop_product.price
        super().save(*args, **kwargs)

class CartItem(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ Add price field

    def save(self, *args, **kwargs):
        """ Automatically set price based on ShopProduct """
        if not self.price:  # Only set price if it's not already provided
            shop_product = ShopProduct.objects.filter(shop=self.shop, product=self.product).first()
            if shop_product:
                self.price = shop_product.price
        super().save(*args, **kwargs)

class OrderRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    shop = models.ForeignKey(ShopProfile, on_delete=models.CASCADE, null=True, blank=True)
    shop_owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # ✅ Add price field

    def approve(self):
        self.status = 'approved'
        self.booking.start_timer()
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()
        
    def save(self, *args, **kwargs):
        if not self.price and self.booking.shop:
            shop_product = ShopProduct.objects.filter(shop=self.booking.shop, product=self.booking.product).first()
            if shop_product:
                self.price = shop_product.price
        super().save(*args, **kwargs)


class BookingRequest(models.Model):
    booking = models.ForeignKey("Booking", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")])
    created_at = models.DateTimeField(auto_now_add=True)  # Track booking time
    duration = models.DurationField(default="1 day")  # Example duration

    @property
    def remaining_time(self):
        expiry_time = self.created_at + self.duration
        remaining = expiry_time - now()
        return max(remaining, None)  # Ensure we don't return negative values
