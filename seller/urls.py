from django.urls import path
from accounts.views import seller_logout
from .views import *
from accounts import views as account_views

app_name = 'seller'

urlpatterns = [
    path('home/', seller_home, name='seller_home'),
    path('login/', account_views.login_user, {'role': 'seller'}, name='login'),
    path('register/', account_views.register_user, {'role': 'seller'}, name='register'),
    
    path('logout/', seller_logout, name='seller_logout'),
    path('delete_item/<int:pk>/', delete_item, name='delete_item'),
    path('delete_deal_item/<int:pk>/', delete_deal_item, name='delete_deal_item'),
    path('main_home/', main_home, name='main_home'),
    

]