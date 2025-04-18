# buyer/forms.py
from django import forms
from .models import Cart

class CartAddForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
        }
