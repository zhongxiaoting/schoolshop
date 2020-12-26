from django import forms

from .models import Product


class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'phone', 'avatar', 'price', 'description')