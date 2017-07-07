from django import forms
from .models import Store, Product
from django.utils import timezone
from django.contrib.auth.models import User

class addForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'price')


class editForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'image', 'description', 'old_price')

class searchForm(forms.Form):
    name = forms.CharField(label = 'name')
    searchType = forms.TypedChoiceField(choices=[(0,'store'),(1,'product'),], initial=0)

class searchProductForm(forms.Form):
    name = forms.CharField(label = 'name', required=False)

class discountProductForm(forms.Form):
    discount = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 11)], initial=10)
