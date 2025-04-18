from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings

from .forms import (
    BuyerRegistrationForm,
    SellerRegistrationForm,
    HomemadeRegistrationForm,
    LoginForm
)
from .models import CustomUser


def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('seller:login')
    else:
        form = SellerRegistrationForm()
    return render(request, 'register.html', {'form': form, 'role': 'seller'})


def buyer_register(request):
    if request.method == 'POST':
        form = BuyerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buyer:login')
    else:
        form = BuyerRegistrationForm()
    return render(request, 'register.html', {'form': form, 'role': 'buyer'})


def homemade_register(request):
    if request.method == 'POST':
        form = HomemadeRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homemade:login')
    else:
        form = HomemadeRegistrationForm()
    return render(request, 'register.html', {'form': form, 'role': 'homemade'})


# ✅ Unified Login View with backend fix
# def login_user(request, role):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             identifier = form.cleaned_data['email_or_phone']
#             password = form.cleaned_data['password']

#             user = CustomUser.objects.filter(email=identifier).first() or \
#                    CustomUser.objects.filter(phone_number=identifier).first()

#             if user and user.check_password(password):
#                 # Check correct role
#                 if ((role == 'buyer' and user.is_buyer) or
#                     (role == 'seller' and user.is_seller) or
#                     (role == 'homemade' and user.is_homemade)):
                    
#                     # ✅ Fix: manually set backend
#                     user.backend = settings.AUTHENTICATION_BACKENDS[0]
#                     login(request, user)

#                     if role == 'buyer':
#                         return redirect('buyer:buyer_home')
#                     elif role == 'seller':
#                         return redirect('seller:seller_home')
#                     elif role == 'homemade':
#                         return redirect('homemade:homemade_home')
#                 else:
#                     messages.error(request, 'Invalid role for this user.')
#             else:
#                 messages.error(request, 'Invalid credentials.')
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form, 'role': role})
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login

def login_user(request, role):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['email_or_phone']
            password = form.cleaned_data['password']

            user = CustomUser.objects.filter(email=identifier).first() or \
                   CustomUser.objects.filter(phone_number=identifier).first()

            if user:
                if user.check_password(password):
                    # Role check
                    if ((role == 'buyer' and user.is_buyer) or
                        (role == 'seller' and user.is_seller) or
                        (role == 'homemade' and user.is_homemade)):

                        # Set backend manually
                        user.backend = settings.AUTHENTICATION_BACKENDS[0]
                        login(request, user)

                        if role == 'buyer':
                            return redirect('buyer:buyer_home')
                        elif role == 'seller':
                            return redirect('seller:seller_home')
                        elif role == 'homemade':
                            return redirect('homemade:homemade_home')
                    else:
                        messages.error(request, 'You are not authorized for this role.')
                else:
                    messages.error(request, 'Invalid password.')
            else:
                messages.error(request, 'User with this email or phone does not exist.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'role': role})


def register_user(request, role):
    if role == 'buyer':
        return buyer_register(request)
    elif role == 'seller':
        return seller_register(request)
    elif role == 'homemade':
        return homemade_register(request)
    else:
        messages.error(request, 'Invalid role specified.')
        return redirect('home')


# Role-based login shortcuts
def buyer_login(request):
    return login_user(request, role='buyer')


def seller_login(request):
    return login_user(request, role='seller')


def homemade_login(request):
    return login_user(request, role='homemade')



from django.contrib.auth import logout
from django.shortcuts import redirect




def buyer_logout(request):
    logout(request)
    return redirect('buyer:login')

def seller_logout(request):
    logout(request)
    return redirect('seller:login')

def homemade_logout(request):
    logout(request)
    return redirect('homemade:login')



from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/')

def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            profile = form.save(commit=False)

            new_password = form.cleaned_data.get('new_password')
            if new_password:
                profile.set_password(new_password)
            profile.save()

            # Keep user logged in after password change
            if new_password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, profile)

            messages.success(request, 'Updated')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)

    # Determine role to display
    if user.is_buyer:
        role = "Buyer"
    elif user.is_seller:
        role = "Seller"
    elif user.is_homemade:
        role = "Homemade"
    else:
        role = "Unknown"

    return render(request, 'profile.html', {
        'form': form,
        'email': user.email,
        'role': role,
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProfileForm

@login_required(login_url='/')

def profile_view(request):
    user = request.user

    if user.is_buyer:
        role = 'buyer'
    elif user.is_seller:
        role = 'seller'
    elif user.is_homemade:
        role = 'homemade'
    else:
        role = None

    # Safely build back_url only if role is known
    if role:
        back_url = f'{role}:{role}_home'
    else:
        back_url = None  # prevent template from erroring

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'profile.html', {
        'form': form,
        'email': user.email,
        'role': role.capitalize() if role else '',
        'back_url': back_url,
    })
