from django.urls import path
from . import views


urlpatterns = [

    # choose the shop to buy the product
    path('choose-shop/<int:product_id>/<str:action>/', views.choose_shop, name='choose_shop'),

    # Create booking
    # path('make_booking/<int:product_id>/<int:shop_id>/', views.make_booking, name='make_booking'),

    # customer view booking
    path('view_bookings/', views.view_bookings, name='view_bookings'),

    # shop owner request list
    path('shop_owner_requests/', views.shop_owner_requests, name='shop_owner_requests'),

    #shop owner request verify
    path('handle_order_request/<int:request_id>/<str:action>/', views.handle_order_request, name='handle_order_request'),

    path('view_cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('booking/remove/<int:item_id>/', views.remove_from_booking, name='remove_from_booking'),
    path('booking/<int:booking_id>/update-payment/', views.update_payment, name='update_payment'),
    path('cart/estimate/', views.estimate, name='estimate'),
    path('checkout/', views.checkout, name='checkout'),
    path("remove-expired-bookings/", views.remove_expired_bookings, name="remove_expired_bookings"),
    path('delete_expired_bookings/', views.delete_expired_bookings, name='delete_expired_bookings'),
    path("update-payment-method/", views.update_payment_method, name="update_payment_method"),
    path('check-phone/', views.check_phone_number, name='check_phone'),
    path('billing/<int:user_id>/', views.billing_page, name='billing_page'),
    

]