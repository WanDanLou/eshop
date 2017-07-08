from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('name',  'email', 'address', 'postal_code', 'city', 'message')

class searchOrderForm(forms.Form):
    paidType = forms.TypedChoiceField(choices=[(0,'None'),(1,'已支付'),(2,'未支付')], initial=0)
    wait_recievedType = forms.TypedChoiceField(choices=[(0,'None'),(1,'已全送达'),(2,'未全送达')], initial=0)
    deletedType = forms.TypedChoiceField(choices=[(0,'None'),(1,'已删除'),(2,'未删除')], initial=0)
    finishedType = forms.TypedChoiceField(choices=[(0,'None'),(1,'已完成'),(2,'未完成')], initial=0)
