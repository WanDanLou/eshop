from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .store_forms import LoginForm, RegisterForm, UserEditForm, StoreEditForm, ChangePassworForm
from .models import Store, Product
from account.models import Profile
from django.contrib import messages
# Create your views here.
@login_required
def index_store(request, store_slug):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    if store.user.id != request.user.id:
        return redirect('index')
    return render(request, 'index_store.html', {'store':store})

def login_store(request):
    user = request.user
    if user.is_authenticated :
        return redirect('index')
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
                        store = get_object_or_404(Store, user=user)
                        auth.login(request, user)
                        return redirect('index')
                else:
                    form = LoginErrorForm()
                    return render(request, 'store/login_store.html',
                                            {'form': form, 'errors':"user has been banned"})
            else:
                if User.objects.filter(email=cd['username']).exists():
                    new_user = User.objects.get(email=cd['username'])
                    user = auth.authenticate(username = new_user.username,
                                            password = cd['password'])
                    if user is not None:
                        if user.is_active:
                            if not user.profile.usertype:
                                return render(request, 'store/login_store.html',
                                                        {'form': form, 'errors':"user is not store"})
                            else:
                                store = get_object_or_404(Store, user=user)
                                auth.login(request, user)
                                return redirect('index_store',store.slug)
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
    user = request.user
    if user.is_authenticated :
        return redirect('index')
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
            if User.objects.filter(email = cd['email']).exists():
                return render(request, 'store/register_store.html',
                                        {'form': form, 'errors':"email has bee occupied"})
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_store = Store.objects.create(user=new_user)
            new_store.slug = cd['storename']
            new_store.name = cd['storename']
            new_store.money = 1000
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
    user = request.user
    if(not user.is_authenticated):
        return redirect('index')
    auth.logout(request)
    return redirecter('account:index.html')

@login_required
def edit_store(request):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    if request.method == 'POST':
        new_user_form = UserEditForm(instance=request.user, data=request.POST)
        new_store_form = StoreEditForm(instance=request.user.store, data=request.POST, files=request.FILES)
        if new_user_form.is_valid() and new_store_form.is_valid():
            new_user_form.save()
            new_store_form.save()
            request.user.store.slug = request.user.store.name
            request.user.store.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your store')
    else:
        new_user_form = UserEditForm(instance=request.user)
        new_store_form = StoreEditForm(instance=request.user.store)
    return render(request, 'store/edit_store.html', {'user_form': new_user_form, 'store_form': new_store_form, 'store':request.user.store})

@login_required
def change_store_password(request):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
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


def list_store(request):
    stores = Store.objects.exclude(products=None)
    return render(request,'store/list_store.html', {'stores':stores})
