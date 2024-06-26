from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock_quantity']


class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['stock_quantity']
