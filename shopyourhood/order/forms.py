from django import forms

from shopyourhood import products
from .models import Booking, CartItem, OrderRequest

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['product', 'shop']  # Include fields you want to expose in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = products.objects.filter(is_verified=True)  # Filter for verified products

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'shop', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = products  .objects.filter(is_verified=True)  # Filter for verified products

class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['booking', 'shop_owner']
