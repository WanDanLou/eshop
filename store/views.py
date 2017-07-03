from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserEditForm, StoreEditForm, ChangePassworForm
from .models import Store
from account.models import Profile
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_store(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = auth.authenticate(username = cd['username'],
                                    password = cd['password'])
            if user is not None:
                if user.is_active:
                    if not user.profile.usertype:
                        return render(request, 'store/login_store.html',
                                                {'form': form, 'errors':"user is not store"})
                    else:
                        auth.login(request, user)
                        return render(request, 'index.html')
                else:
                    form = LoginErrorForm()
                    return render(request, 'store/login_store.html',
                                            {'form': form, 'errors':"user has been banned"})
        return render(request, 'store/login_store.html',
                                            {'form': form, 'errors':"wrong username or wrong password"})
    else:
        form = LoginForm()
        return render(request, 'store/login_store.html',{'form': form})

def register_store(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password2']:
                return render(request, 'store/register_store.html',
                                        {'form': form, 'errors':"two password are not same"})
            username_exists=User.objects.filter(username=cd['username']).exists()
            if username_exists:
                return render(request, 'store/register_store.html',
                                        {'form': form, 'errors':"username has existed"})
            storename_exists=Store.objects.filter(name = cd['storename']).exists()
            if storename_exists:
                return render(request, 'store/register_store.html',
                                        {'form': form, 'errors':"storename has existed"})
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_store = Store.objects.create(user=new_user)
            new_store.slug = cd['storename']
            new_store.name = cd['storename']
            new_store.save()
            new_profile = Profile.objects.create(user=new_user)
            new_profile.usertype = True
            new_profile.save()
            return render(request, 'store/register_store_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()
        return render(request, 'store/register_store.html', {'form': form})

@login_required
def logout_store(request):
    auth.logout(request)
    return render(request, 'index.html')

@login_required
def edit_store(request):
    if request.method == 'POST':
        new_user_form = UserEditForm(instance=request.user, data=request.POST)
        new_store_form = StoreEditForm(instance=request.user.store, data=request.POST, files=request.FILES)
        if new_user_form.is_valid() and new_store_form.is_valid():
            new_user_form.save()
            new_store_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your store')
    else:
        new_user_form = UserEditForm(instance=request.user)
        new_store_form = StoreEditForm(instance=request.user.store)
    return render(request, 'store/edit_store.html', {'user_form': new_user_form, 'store_form': new_store_form})

@login_required
def change_password_store(request):
    if request.method == 'POST':
        form = ChangePassworForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            now_user = request.user
            if auth.authenticate(username = now_user.username, password = cd['old_password']):
                if cd['new_password1'] != cd['new_password2']:
                    messages.error(request, 'two password are not same')
                else:
                    now_user.set_password(cd['new_password1'])
                    now_user.save()
                    auth.login(request, now_user)
                    messages.success(request, 'change successfully')
            else:
                messages.error(request, 'old password wrong')
    else:
        form = ChangePassworForm()
    return render(request, 'store/change_store_password.html', {'form':form})
