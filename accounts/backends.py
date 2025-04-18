# accounts/backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class EmailOrPhoneBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        
        # Try to find the user by email or phone
        user = None
        if username:
            try:
                if '@' in username:  # If it's an email
                    user = User.objects.get(email=username)
                else:  # If it's a phone number
                    user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        
        if user and user.check_password(password):
            return user
        
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
