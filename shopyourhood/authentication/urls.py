from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Customer registration
    path('register/customer/', views.customer_register, name='customer_register'),

    # view and edit customer info
    path('customer/profile', views.view_customer_profile, name='view_customer_profile'),
    path('customer/profile/edit/', views.edit_customer_profile, name='edit_customer_profile'),



    # Shop owner registration
    path('register/shop/', views.shop_owner_register, name='shop_owner_register'),

    # Dashboards
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('shop/dashboard/', views.shop_owner_dashboard, name='shop_owner_dashboard'),

    # Shop pending verification
    path('shop/pending_verification/', views.shop_pending_verification, name='shop_pending_verification'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
     path('logout/', auth_views.custom_logout, name='logout'),


     # Admin dashboard (for verifying shops)
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    #Veryfing shop list
    path('admin/shop_verify_list/', views.shop_verify_list, name='shop_verify_list'),

    # Verify or reject a shop
    path('admin/verify_shop/<int:shop_id>/', views.verify_shop, name='verify_shop'),
]   