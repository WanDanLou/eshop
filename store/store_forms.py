from django import forms
from .models import Store
from django.utils import timezone
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label = 'username')
    password = forms.CharField(label = 'password',widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField(label = 'username')
    storename = forms.CharField(label = 'storename')
    email = forms.EmailField()
    password = forms.CharField(label = 'password', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'password repeat',widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class StoreEditForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ('name', 'photo', 'description')

class ChangePassworForm(forms.Form):
    old_password = forms.CharField(label = 'old password',widget=forms.PasswordInput)
    new_password1 = forms.CharField(label = 'new password',widget=forms.PasswordInput)
    new_password2 = forms.CharField(label = 'repeat new password',widget=forms.PasswordInput)
