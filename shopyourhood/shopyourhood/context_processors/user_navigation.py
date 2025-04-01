# context_processors/user_navigation.py

def user_navigation(request):
    navigation = []
    sidebar = []
    
    if request.user.is_authenticated:
        user_type = request.user.user_type  # Assuming user_type is an integer
        if user_type == 1:  # Customer
            navigation = [ 
                
                # {'name': 'Cart', 'url': 'view_cart', 'icon': 'fas fa-shopping-cart'},
                {'name': 'Logout', 'url': 'logout', 'icon': 'fas fa-sign-out-alt'},
            ]
            sidebar = [
                {'name': 'Dashboard', 'url': 'customer_dashboard', 'icon': 'fas fa-tachometer-alt'},
                {'name': 'Profile', 'url': 'view_customer_profile', 'icon': 'fas fa-user'},
                {'name': 'Carts', 'url': 'view_cart', 'icon': 'fa-solid fa-cart-shopping'},
                {'name': 'Bookings', 'url': 'view_bookings', 'icon': 'fas fa-calendar-check'},
                
                
            ]
        elif user_type == 2:  # Shop Owner
            navigation = [
                {'name': 'Logout', 'url': 'logout', 'icon': 'fas fa-sign-out-alt'},
            ]
            sidebar = [
                {'name': 'Dashboard', 'url': 'shop_owner_dashboard', 'icon': 'fas fa-tachometer-alt'},
                {'name': 'Add Product', 'url': 'search_verified_products', 'icon': 'fas fa-plus'},
                {'name': 'My Products', 'url': 'view_verified_products', 'icon': 'fas fa-box'},
                {'name': 'Pending', 'url': 'view_pending_requests', 'icon': 'fas fa-clock'},
                {'name': 'Orders', 'url': 'shop_owner_requests', 'icon': 'fas fa-shopping-cart'},
            ]
        elif user_type == 3:  # Admin
            navigation = [
                {'name': 'Logout', 'url': 'logout', 'icon': 'fas fa-sign-out-alt'},
            ]
            sidebar = [
                {'name': 'Dashboard', 'url': 'admin_dashboard', 'icon': 'fas fa-tachometer-alt'},
                {'name': 'Shop Verify', 'url': 'shop_verify_list', 'icon': 'fas fa-check-circle'},
                {'name': 'Product Verify', 'url': 'product_verify_list', 'icon': 'fas fa-check-circle'},
            ]
    else:
        navigation = [
            
            {'name': 'Register', 'url': '#', 'icon': 'fas fa-user-plus'},
            {'name': 'Login', 'url': 'login', 'icon': 'fas fa-sign-in-alt'},
        ]
        sidebar = [
            # {'name': '', 'url': 'about', 'icon': 'fas fa-info-circle'},
            # {'name': 'Contact', 'url': '#', 'icon': 'fas fa-envelope'},
        ]

    return {
        'navigation': navigation,
        'sidebar': sidebar,
    }
