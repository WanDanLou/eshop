from django import forms
from .models import Store, Product
from django.utils import timezone
from django.contrib.auth.models import User

class addForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'stock')


class editForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price', 'stock')
