from django.urls import path
# from .views import buyer_home
from accounts import views as account_views
from accounts.views import buyer_logout

from . import views



from django.urls import path
from . import views

app_name = 'buyer'

urlpatterns = [
    path('home/', views.buyer_home, name='buyer_home'),
    path('login/', account_views.login_user, {'role': 'buyer'}, name='login'),
    path('register/', account_views.register_user, {'role': 'buyer'}, name='register'),
    path('logout/', buyer_logout, name='buyer_logout'),
    path('cart/', views.cart_view, name='cart'),  # Corrected to match views.cart_view

    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('delete-from-cart/<int:item_id>/', views.delete_from_cart, name='delete_from_cart'),
    path('update-cart/', views.update_cart_bulk, name='update_cart_bulk'),
    path('order/', views.order_summary, name='order'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-history/', views.order_history, name='order_history'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('checkout/', views.checkout_view, name='checkout'),

]



# buyer/urls.py
# from django.urls import path
# from . import views

# app_name = 'buyer'

# urlpatterns = [
#     path('', views.buyer_home, name='home'),
#     path('cart/', views.cart, name='cart'),
#     path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
#     path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
#     path('checkout/', views.checkout, name='checkout'),
#     path('order/', views.order_view, name='order'),
# ]
