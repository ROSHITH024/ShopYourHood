from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_verified_products, name='search_verified_products'),
    path('add/<int:product_id>/', views.add_product_to_shop, name='add_product_to_shop'),
    path('register/', views.register_product, name='register_product'),
    
    # verification section 
    path('verify/product_pending_verification/', views.product_pending_verification, name='product_pending_verification'),
    path('verify/product_verify_list/', views.product_verify_list, name='product_verify_list'),
    path('verify/<int:product_id>/', views.verify_product, name='verify_product'),

    # URLs shop's product viewing
    path('view_verified_products/', views.view_verified_products, name='view_verified_products'),

    # URLs shop's product editing and deleting 
    path('view_pending_requests/edit/<int:product_id>/', views.edit_shop_product, name='edit_shop_product'),
    path('view_pending_requests/delete/<int:product_id>/', views.delete_shop_product, name='delete_shop_product'),

     # shop pending requests
    path('view_pending_requests/', views.view_pending_requests, name='view_pending_requests'),

    
   
    # path('customer/products/', views.customer_view_verified_products, name='customer_view_verified_products'),
]
