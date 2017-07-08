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

CATEGORY_CHOICES =[(1,'不知道怎么分类'), (2,'攻击'), (3,'法术'), (4,'防御'), (5,'移动'), (6, '打野及消耗品')]
class categoryForm(forms.Form):
    category=forms.TypedChoiceField(choices=CATEGORY_CHOICES, initial=1)

class searchForm(forms.Form):
    name = forms.CharField(label = 'name', required=False)
    searchType = forms.TypedChoiceField(choices=[(0,'store'),(1,'product'),], initial=1)
    sortType = forms.TypedChoiceField(choices=[(0,'created'),(1,'price'),(2,'volume')], initial=0)
    filterType = forms.TypedChoiceField(choices=[(0,'None'),(1,'不知道怎么分类'), (2,'攻击'), (3,'法术'), (4,'防御'), (5,'移动'), (6, '打野及消耗品')], initial=0)
    orderType = forms.TypedChoiceField(choices=[(0,'升序'),(1,'降序')], initial=0)

class searchProductForm(forms.Form):
    name = forms.CharField(label = 'name', required=False)

class discountProductForm(forms.Form):
    discount = forms.TypedChoiceField(choices=[(i, str(i)) for i in range(1, 11)], initial=10)
