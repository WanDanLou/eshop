from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm, UserEditForm, ProfileEditForm, ChangePassworForm,ProductCreateForm
from cart.forms import CartAddProductForm
from .models import Profile,Category,Product
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.
def index(request):
    return render(request, 'index.html')
def login_user(request):
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
                        return render(request, 'index.html')
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
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_profile = Profile.objects.create(user=new_user)
            #new_profile.save()
            return render(request, 'account/register_user_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()
        return render(request, 'account/register_user.html', {'form': form})

@login_required
def logout_user(request):
    auth.logout(request)
    return render(request, 'index.html')

@login_required
def edit_user(request):
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

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'account/list.html',
                  {'category': category,
                  'categories': categories,
                  'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                'account/detail.html',
                {'product': product,'cart_product_form': cart_product_form})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] != cd['password2']:
                return render(request, 'account/register.html',
                                        {'form': form, 'errors':"two password are not same"})
            username_exists=User.objects.filter(username=cd['username']).exists()
            if username_exists:
                return render(request, 'account/register.html',
                                        {'form': form, 'errors':"username has existed"})
            new_user = User()
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email =cd['email']
            new_user.save()
            new_profile = Profile.objects.create(user=new_user)
            #new_profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        form = RegisterForm()
        return render(request, 'account/register.html', {'form': form})

@login_required
def product_create(request):
    if request.method == 'POST':
        # form is sent
        product_create_form = ProductCreateForm(data=request.POST)
        if product_create_form.is_valid():
            cd = form.cleaned_data
            category_exists=User.objects.filter(slug=cd['categoryslug']).exists()
            if username_exists:
                new_category = Category.objects.filter(slug=cd['categoryslug'])
            else:
                new_category = Category()
                new_category.name = cd['categoryname']
                new_category.slug = cd['categoryslug']
                new_category.save()
            new_product = Product.objects.create(category=_category)
            new_product.productname = cd['productname']
            new_product.productslug = cd['productslug']
            new_product.description = cd['description']
            new_product.price = cd['price']
            new_product.stock = cd['stock']
            new_product.save()
            product_create_form.save()
            messages.success(request, 'Product added successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        # build form with data provided by the bookmarklet via GET
        product_create_form = ProductCreateForm(data=request.GET)
    return render(request, 'account/create.html', {'product_create_form': product_create_form})
