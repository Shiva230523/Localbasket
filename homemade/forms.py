from django import forms
from .models import HomeMadeItem

# class HomeMadeItemForm(forms.ModelForm):
#     class Meta:
#         model = HomeMadeItem
#         fields = ['item', 'price', 'address', 'image']
#         widgets = {
#             'item': forms.TextInput(attrs={'placeholder': 'Item name'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
#             'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your address'}),
#         }

from django import forms
from .models import HomeMadeItem

class HomeMadeItemForm(forms.ModelForm):
    class Meta:
        model = HomeMadeItem
        fields = ['item', 'price', 'address', 'image', 'order_limit']
        widgets = {
            'item': forms.TextInput(attrs={'placeholder': 'Item name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price'}),
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your address'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'order_limit': forms.NumberInput(attrs={'placeholder': 'Maximum number of orders'}),
        }