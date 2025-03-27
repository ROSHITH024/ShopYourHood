from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import CustomerRegistrationForm, ShopOwnerRegistrationForm,CustomerProfileForm
from django.contrib.auth.decorators import login_required
from .models import ShopProfile,CustomUser
from order.models import Booking
import os
from products.models import Product

# from django.utils.decorators import method_decorator
# from django.views.decorators.cache import never_cache

# Customer registration view
def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to customer login page
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register/customer_register.html', {'form': form})

# Shop owner registration view
def shop_owner_register(request):
    if request.method == 'POST':
        form = ShopOwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')   # Redirect to verification page
    else:
        form = ShopOwnerRegistrationForm()
    return render(request, 'register/shop_owner_register.html', {'form': form})


# customer dashboard 
@login_required
def customer_dashboard(request):
    if request.user.user_type != 1:  # Ensure only customer can access this view
        return redirect('login')
    verified_products = Product.objects.filter(is_verified=True).order_by('category')  # Fetch verified products
    categories = {}

    # Organize products by category
    for product in verified_products:
        category_name = product.category
        if category_name not in categories:
            categories[category_name] = []
        categories[category_name].append(product)
    return render(request, 'dashboard/customer_dashboard.html', {'categories': categories})




# Shop Dashboard 
@login_required
def shop_owner_dashboard(request):
    shop_profile = request.user.shopprofile
    
    if not shop_profile.is_verified:
        return redirect('shop_pending_verification')  # Redirect to a pending verification page
    return render(request, 'dashboard/shop_owner_dashboard.html',{'shop_profile':shop_profile})


# shop pending verification
@login_required
def shop_pending_verification(request):
    try:
        # Check if the user has a shopprofile
        shop_profile = request.user.shopprofile
        name = shop_profile.name  # Shop name field
        print(name,'--------------')
    except AttributeError:
        # Handle the case if the shopprofile does not exist
        name = "Shop Owner"  # Default or fallback name
    return render(request, 'verify/shop_pending_verification.html',{'name':name})


# users login 

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user
        if user.user_type == 1:  # Customer
            return reverse('customer_dashboard')
        elif user.user_type == 2:  # Shop Owner
            return reverse('shop_owner_dashboard')
        elif user.user_type == 3: # admin
            return reverse('admin_dashboard')
        
        
# Admin dashboard view (list of pending shop owners)
@login_required
def admin_dashboard(request):
    # Fetch the total number of customers and shop owners
    total_users = CustomUser.objects.filter(Q(user_type=1) | Q(user_type=2)).count()

    # Fetch the total number of active orders (approved orders)
    active_orders = Booking.objects.filter(status='approved').count()

    # Fetch the total number of pending shop and product verification requests
    pending_shop_verifications = ShopProfile.objects.filter(is_verified=False).count()
    pending_product_verifications = Product.objects.filter(is_verified=False).count()
    pending_requests = pending_shop_verifications + pending_product_verifications

    name = request.user.username
    return render(request, 'dashboard/admin_dashboard.html', {
        'name': name,
        'total_users': total_users,
        'active_orders': active_orders,
        'pending_requests': pending_requests,
    })


# Admin dashboard view (list of pending shop owners)
@login_required
def shop_verify_list(request):
    if request.user.user_type != 3:  # Ensure only admin can access this view
        return redirect('login')

    # List all unverified shop owners
    unverified_shops = ShopProfile.objects.filter(is_verified=False).select_related('user')
    return render(request, 'verify/Shop_verify_list.html', {'unverified_shops': unverified_shops})

# View to verify or reject a shop
@login_required
def verify_shop(request, shop_id):
    if request.user.user_type != 3:  # Ensure only admin can access this view
        return redirect('login')

    shop = get_object_or_404(ShopProfile, id=shop_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'verify':
            shop.is_verified = True
            shop.save()
        elif action == 'reject':
            # Delete both the ShopProfile and associated CustomUser
            # Delete the shop proof image if it exists
            if shop.shop_proof:
                if os.path.isfile(shop.shop_proof.path):
                    os.remove(shop.shop_proof.path)

            user = shop.user  # Get the associated CustomUser
            user.delete()  # This will also delete the ShopProfile due to on_delete=models.CASCADE
        return redirect('admin_dashboard')

    return render(request, 'verify/verify_shop.html', {'shop': shop})




# customer profile view 
@login_required
def view_customer_profile(request):
    profile = request.user.customerprofile  # Get the logged-in user's profile
    return render(request, 'customer/profile.html', {'profile': profile})

@login_required
def edit_customer_profile(request):
    profile = request.user.customerprofile
    user = request.user  # Get the CustomUser instance

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile, user_instance=user)
        if form.is_valid():
            form.save()
            return redirect('view_customer_profile')  # Redirect to the profile view after saving
    else:
        form = CustomerProfileForm(instance=profile, user_instance=user)
    return render(request, 'customer/edit_profile.html', {'form': form})