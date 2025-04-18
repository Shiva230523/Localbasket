# seller/decorators.py

from functools import wraps
from django.shortcuts import redirect

def seller_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'is_seller', False):
            return redirect('seller:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
