from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Product, Order




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'discount', 'image', 'category']


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'name', 'phone', 'quantity']


