# accounts/urls.py
from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    # path('login/buyer/', views.buyer_login, name='buyer_login'),
    path('login/seller/', views.seller_login, name='seller_login'),
    path('login/homemade/', views.homemade_login, name='homemade_login'),
    path('login/buyer/', views.buyer_login, name='buyer_login'),
    path('register/seller/', views.seller_register, name='register-seller'),
    path('login/', views.login_user, name='login'),
    path('register/buyer/', views.buyer_register, name='register-buyer'),
    # path('register', views.seller_register, name='seller_register'),
    path('register/homemade/', views.homemade_register, name='register-homemade'),
    path('profile/', views.profile_view, name='profile'),
]
