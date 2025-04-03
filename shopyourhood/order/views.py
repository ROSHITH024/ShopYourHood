from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from authentication import models
from .models import Booking, BookingRequest, CartItem, OrderRequest
from products.models import Product, ShopProduct
from django.urls import reverse
from authentication.models import ShopProfile
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.http import HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

@login_required
def choose_shop(request, product_id, action):
    product = get_object_or_404(Product, id=product_id, is_verified=True)
    shop_products = ShopProduct.objects.filter(product=product)

    if request.method == 'POST':
        shop_id = request.POST.get('shop_id')
        quantity = request.POST.get('quantity', 1)

        if not shop_id:
            return HttpResponseBadRequest("Shop ID is required")

        shop_product = ShopProduct.objects.filter(shop_id=shop_id, product=product).first()
        shop = get_object_or_404(ShopProfile, id=shop_id)  # ✅ Fetch ShopProfile object

        if action == 'cart':
            CartItem.objects.create(
                customer=request.user, 
                product=product, 
                shop=shop,  # ✅ Use shop object
                quantity=int(quantity)
            )
            return redirect(reverse('view_cart'))

        elif action == 'book':
            booking = Booking.objects.create(
                customer=request.user, 
                product=product, 
                shop=shop,  # ✅ Use shop object
                status='pending',
                price=shop_product.price if shop_product else None
            )
            booking.start_timer()

            try:
                shop_owner = shop.user  # ✅ Get shop owner
                OrderRequest.objects.create(booking=booking, shop=shop, shop_owner=shop_owner)
            except ShopProfile.DoesNotExist:
                return HttpResponseBadRequest("Invalid shop selection")

            return redirect('view_bookings')

    return render(request, 'order/choose_shop.html', {
        'product': product,
        'shop_products': shop_products,
        'action': action
    })

# cart
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)  # Get cart items for the logged-in user
    total_price = 0

    for item in cart_items:
        # Fetch the ShopProduct for each item in the cart
        try:
            shop_product = ShopProduct.objects.get(product=item.product, shop=item.shop)
            item.price = shop_product.price  # Store the price of the product
            item.total_item_price = shop_product.price * item.quantity  # Calculate total price for this item
            total_price += item.total_item_price  # Add to the overall total price
        except ShopProduct.DoesNotExist:
            item.price = 0  # Default price if not found
            item.total_item_price = 0  # Default total item price if not found

    return render(request, 'order/view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })





@login_required
@require_POST
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        # Get the cart item to be removed
        cart_item = get_object_or_404(CartItem, id=item_id, customer=request.user)
        cart_item.delete()  # Remove the item from the cart

    return redirect('view_cart')  # Redirect back to the cart view


@login_required
@require_POST
def remove_from_booking(request, item_id):
    if request.method == 'POST':
        # Get the cart item to be removed
        book_item = get_object_or_404(Booking, id=item_id, customer=request.user)
        book_item.delete()  # Remove the item from the booking

    return redirect('view_bookings')  # Redirect back to the booking view




@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    
    for item in cart_items:
        # Create individual bookings based on the item's quantity
        for _ in range(item.quantity):
            booking = Booking.objects.create(
                customer=request.user,
                product=item.product,
                shop=item.shop,
                status='pending',
                price=ShopProduct.price if ShopProduct else None 
            )
            
            # Start the 24-hour timer on each booking
            booking.start_timer()
            
            # Create an order request tied to the booking for shop approval
            OrderRequest.objects.create(bookingOrderRequest=booking, shop_owner=item.shop.user)
    
    # Clear cart after checkout
    cart_items.delete()
    
    return redirect('view_bookings')

@login_required
def estimate(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = 0
    item_calculations = []

    for item in cart_items:
        # Fetch the ShopProduct to get the correct price
        try:
            shop_product = ShopProduct.objects.get(product=item.product, shop=item.shop)
            item_price = shop_product.price * item.quantity
            total_price += item_price
            item_calculations.append({
                'product_name': item.product.name,
                'quantity': item.quantity,
                'unit_price': shop_product.price,
                'total_price': item_price
            })
        except ShopProduct.DoesNotExist:
            continue  # Skip if the shop product isn't found

    return render(request, 'order/estimate.html', {
        'item_calculations': item_calculations,
        'total_price': total_price,
    })





# Create booking

# @login_required
# def make_booking(request, product_id, shop_id):
#     product = get_object_or_404(Product, id=product_id)
#     shop = get_object_or_404(ShopProfile, id=shop_id)
#     booking = Booking(customer=request.user, product=product, shop=shop, status='pending')
#     booking.save()

#     booking.start_timer()

#     shop_owner = shop.user
#     OrderRequest.objects.create(booking=booking, shop_owner=shop_owner)
#     return redirect('view_bookings')


# customer view booking
@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(customer=request.user)
    return render(request, 'order/view_bookings.html', {'bookings': bookings})



# shop owner request list
@login_required
def shop_owner_requests(request):
    requests = OrderRequest.objects.filter(shop_owner=request.user)
    for req in requests:
        if req.booking.expires_at:  # Check if expires_at is not None
            req.remaining_time = req.booking.expires_at - timezone.now()
        else:
            req.remaining_time = None  # or set to zero/another default value if needed
    return render(request, 'order/shop_owner_requests.html', {'requests': requests})




#shop owner request verify
@login_required
def handle_order_request(request, request_id, action):
    order_request = get_object_or_404(OrderRequest, id=request_id, shop_owner=request.user)
    if action == 'approve':
        # Update the OrderRequest status to 'approved'
        order_request.status = 'approved'
        order_request.save()

        # Update the related Booking status to 'approved'
        booking = order_request.booking
        booking.status = 'approved'
        booking.save()
    elif action == 'reject':
        booking_id = order_request.booking.id  # Store booking ID for deletion
        order_request.reject()
        booking = order_request.booking
        booking.status = 'reject'
        booking.save()
        # order_request.delete()  # Delete the order request from the OrderRequest table
        # Booking.objects.filter(id=booking_id).delete()
    return redirect('shop_owner_requests')


def remove_expired_bookings(request):
    expired_bookings = Booking.objects.filter(expires_at__lt=now())  # Select expired bookings
    deleted_count, _ = expired_bookings.delete()  # Delete and get the count

    return JsonResponse({"message": f"Removed {deleted_count} expired bookings."})


@csrf_exempt  # Use this only if needed; better to use CSRF token in AJAX
def delete_expired_bookings(request):
    if request.method == "GET":  # Only allow GET requests
        expired_bookings = Booking.objects.filter(status="pending", expires_at__lt=now())
        deleted_count, _ = expired_bookings.delete()

        return JsonResponse({"message": f"Removed {deleted_count} expired pending bookings."})

    return JsonResponse({"error": "Invalid request method."}, status=400)