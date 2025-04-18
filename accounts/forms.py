# # accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


from django import forms
from .models import CustomUser

class BuyerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_buyer = True
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user


class SellerRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_seller = True
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user


class HomemadeRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'email', 'phone_number', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_homemade = True
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user


class LoginForm(forms.Form):
    email_or_phone = forms.CharField(label='Email or Phone', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)





# accounts/forms.py
# from django import forms
# from .models import CustomUser

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'address', 'phone_number']  # 🔒 Exclude email

#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields['phone_number'].required = True

from django import forms
from .models import CustomUser

class ProfileForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password', 
        required=False, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Leave blank to keep current password'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = True














