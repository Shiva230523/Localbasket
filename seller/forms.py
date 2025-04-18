# seller/forms.py

from django import forms
from .models import SellerItem

# class SellerItemForm(forms.ModelForm):
#     class Meta:
#         model = SellerItem
#         fields = ['item', 'price', 'address']
from django import forms
from .models import SellerItem

class SellerItemForm(forms.ModelForm):
    class Meta:
        model = SellerItem
        fields = ['item', 'price', 'address', 'image']



