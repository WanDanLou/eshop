from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm, ChangePassworForm
from .models import Profile
from store.models import Product,Store
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype :
        return redirect("index_store", user.store.slug)
    products = Product.objects.order_by('volume')
    paginator = Paginator(products,4)
    products_order_by_time = Product.objects.order_by('created')
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html',{'products_page': products_page , 'products_order_by_time': products_order_by_time,})
def login_user(request):
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
                    if user.profile.usertype:
                        return render(request, 'account/login_user.html',
                                                {'form': form, 'errors':"user is store"})
                    else:
                        auth.login(request, user)
                        return redirect('index')
                else:
                    form = LoginErrorForm()
                    return render(request, 'account/login_user.html',
                                            {'form': form, 'errors':"user has been banned"})
            else:
                if User.objects.filter(email=cd['username']).exists():
                    new_user = User.objects.get(email=cd['username'])
                    user = auth.authenticate(username = new_user.username,
                                            password = cd['password'])
                    if user is not None:
                        if user.is_active:
                            if user.profile.usertype:
                                return render(request, 'account/login_user.html',
                                                        {'form': form, 'errors':"user is store"})
                            else:
                                auth.login(request, user)
                                for product in user.product_visit.all():
                                    user.product_visit.remove(product)
                                return redirect('index')
                        else:
                            form = LoginErrorForm()
                            return render(request, 'account/login_user.html',
                                                    {'form': form, 'errors':"user has been banned"})
        return render(request, 'account/login_user.html',
                                            {'form': form, 'errors':"wrong username or wrong password"})
    else:
        form = LoginForm()
        return render(request, 'account/login_user.html',{'form': form})

def register_user(request):
    user = request.user
    if user.is_authenticated :
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password2']:
                return render(request, 'account/register_user.html',
                                        {'form': form, 'errors':"two password are not same"})
            username_exists=User.objects.filter(username=cd['username']).exists()
            if username_exists:
                return render(request, 'account/register_user.html',
                                        {'form': form, 'errors':"username has existed"})
            '''if User.objects.filter(email = cd['email']).exists():
                return render(request, 'account/register_user.html',
                                    {'form': form, 'errors':"email has bee occupied"})'''
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_profile = Profile.objects.create(user=new_user, money=1000)
            #new_profile.save()
            return render(request, 'account/register_user_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()
        return render(request, 'account/register_user.html', {'form': form})

@login_required
def logout_user(request):
    user = request.user
    if(not user.is_authenticated):
        return redirect('index')
    auth.logout(request)
    return redirect('index')

@login_required
def edit_user(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    if request.method == 'POST':
        new_user_form = UserEditForm(instance=request.user, data=request.POST)
        new_profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if new_user_form.is_valid() and new_profile_form.is_valid():
            new_user_form.save()
            new_profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        new_user_form = UserEditForm(instance=request.user)
        new_profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit_user.html', {'user_form': new_user_form, 'profile_form': new_profile_form})

@login_required
def change_user_password(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
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
    return render(request, 'account/change_user_password.html', {'form':form})
