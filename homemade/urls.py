from django.urls import path
from .views import homemade_home
from accounts import views as account_views
from accounts.views import homemade_logout
from . import views

app_name = 'homemade'
urlpatterns = [
    path('home/', homemade_home, name='homemade_home'),
    path('login/', account_views.login_user, {'role': 'homemade'}, name='login'),
    path('register/', account_views.register_user, {'role': 'homemade'}, name='register'),
    path('logout/', homemade_logout, name='homemade_logout'),
    path('delete/<int:pk>/', views.delete_homemade_item, name='delete_homemade_item'),
    path('order-requests/', views.order_requests, name='order_requests'),

]

