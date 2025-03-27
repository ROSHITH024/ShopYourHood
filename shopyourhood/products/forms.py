from django import forms
from .models import Product, ShopProduct

# class ProductForm(forms.ModelForm):
    # class Meta:
    #     model = Product
    #     fields = ['name', 'quantity', 'price', 'category', 'description', 'image']
    #     widgets = {
    #         'category': forms.Select(attrs={'class': 'form-control'}),  # Category dropdown
    #         'name': forms.TextInput(attrs={'class': 'form-control'}),
    #         'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
    #         'price': forms.NumberInput(attrs={'class': 'form-control'}),
    #         'description': forms.Textarea(attrs={'class': 'form-control'}),
    #         'image': forms.FileInput(attrs={'class': 'form-control-file'}),
    #     }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'image']

class ShopProductForm(forms.ModelForm):
    class Meta:
        model = ShopProduct
        fields = ['quantity', 'price']