from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, ShopProduct
from .forms import ProductForm, ShopProductForm
from authentication.models import ShopProfile
import os
from django.conf import settings

# Ensure access only for shop owners (user_type=2)
def shop_owner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == 2:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return _wrapped_view



@login_required
@shop_owner_required
def search_verified_products(request):
    query = request.GET.get('query', '')  # Get the query from GET request
    products = Product.objects.filter(is_verified=True, name__icontains=query) if query else None

    # If no products found, show message but don't redirect
    if query and not products.exists():
        messages.info(request, "No matching verified products found. You can register a new product.")

    return render(request, 'product/search_verified_products.html', {'products': products, 'query': query})




@login_required
@shop_owner_required
def add_product_to_shop(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    shop = request.user.shopprofile

    # Check if the product is already in shop's inventory
    if ShopProduct.objects.filter(shop=shop, product=product).exists():
        messages.info(request, "Product is already in your shop.")
        return redirect('search_verified_products')
    else:
        # Create a ShopProduct entry if not already added
        if request.method == 'POST':
            form = ShopProductForm(request.POST)
            if form.is_valid():
                shop_product = form.save(commit=False)
                shop_product.shop = shop
                shop_product.product = product
                shop_product.save()
                messages.success(request, "Product added to your shop.")
                return redirect('view_verified_products')
        else:
            form = ShopProductForm()
        return render(request, 'product/add_product_to_shop.html', {'form': form, 'product': product})



@login_required
@shop_owner_required
def register_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        
        # Check for duplicate product registration by name and shop
        existing_product = Product.objects.filter(
            name__iexact=form['name'].value(),
            added_by=request.user.shopprofile
        ).first()
        
        if existing_product:
            messages.error(request, "This product is already registered.")
            return redirect('search_verified_products')  # Redirect to the shop dashboard or desired page

        if form.is_valid():
            product = form.save(commit=False)
            product.added_by = request.user.shopprofile
            product.is_verified = False  # Set as unverified by default
            product.save()
            messages.success(request, "Product submitted for verification.")
            return redirect('view_pending_requests')  # Redirect to the shop dashboard or desired page
    else:
        form = ProductForm()
        
    return render(request, 'product/register_product.html', {'form': form})



# Admin view of verify list of product 
@login_required
def product_verify_list(request):
    if request.user.user_type != 3:  # Ensure only admin can access this view
        return redirect('login')

    # List all unverified shop owners
    unverified_products = Product.objects.filter(is_verified=False)
    return render(request, 'verify/product_verify_list.html', {'unverified_products': unverified_products})

# pending product verification page

@login_required
def product_pending_verification(request):
    try:
        # Check if the user has a shopprofile
        products = request.user.product
        name = products.name  # Shop name field
        print(name,'--------------')
    except AttributeError:
        # Handle the case if the shopprofile does not exist
        name = "Product"  # Default or fallback name
    return render(request, 'verify/product_pending_verification.html',{'name':name})



# Admin view to verify or reject products, deleting images upon rejection
@login_required
def verify_product(request, product_id):
    if request.user.user_type != 3:  # Ensure only admin can access this view
        return redirect('login')
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'verify':
            product.is_verified = True
            product.save()
            messages.success(request, "Product verified.")
            return redirect('admin_dashboard')
        elif action == 'reject':
            # Delete product image file
            if product.image and os.path.isfile(product.image.path):
                os.remove(product.image.path)
            product.delete()
            messages.info(request, "Product rejected and deleted.")
            return redirect('admin_dashboard')
    return render(request, 'verify/verify_product.html', {'product': product})


# shop view for seeing the product 
@login_required
@shop_owner_required
def view_verified_products(request):
    shop = request.user.shopprofile
    # Fetching verified products linked to the shop
    verified_products = ShopProduct.objects.filter(shop=shop)
    return render(request, 'product/view_verified_products.html', {'verified_products': verified_products})


# shop view for edit the product 
@login_required
@shop_owner_required
def edit_shop_product(request, product_id):
    shop_product = get_object_or_404(ShopProduct, id=product_id, shop=request.user.shopprofile)
    if request.method == 'POST':
        form = ShopProductForm(request.POST, instance=shop_product)
        if form.is_valid():
            form.save()
            return redirect('view_verified_products')
    else:
        form = ShopProductForm(instance=shop_product)
    return render(request, 'product/edit_shop_product.html', {'form': form, 'shop_product': shop_product})



# shop view for delete the product 
@login_required
@shop_owner_required
def delete_shop_product(request, product_id):
    shop_product = get_object_or_404(ShopProduct, id=product_id, shop=request.user.shopprofile)
    if request.method == 'POST':
        shop_product.delete()
        return redirect('view_verified_products')
    return render(request, 'product/confirm_delete.html', {'shop_product': shop_product})





@login_required
@shop_owner_required
def view_pending_requests(request):
    # Fetch products added by the shop that are not verified yet
    pending_products = Product.objects.filter(added_by=request.user.shopprofile, is_verified=False)
    return render(request, 'product/view_pending_requests.html', {'pending_products': pending_products})







