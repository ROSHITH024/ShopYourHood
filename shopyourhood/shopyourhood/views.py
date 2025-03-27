from ast import Return
from os import name
from django.shortcuts import render
from products.models import Product

def index(request):
    verified_products = Product.objects.filter(is_verified=True).order_by('category')  # Fetch verified products
    categories = {}

    # Organize products by category
    for product in verified_products:
        category_name = product.category
        if category_name not in categories:
            categories[category_name] = []
        categories[category_name].append(product)
    return render(request,'index.html',{'categories': categories})
def about(request):
    return render(request,'about.html')