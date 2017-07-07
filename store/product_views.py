from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .product_forms import addForm, editForm, searchForm, searchProductForm, discountProductForm
from cart.forms import CartAddProductForm
from .models import Store, Product
from account.models import Profile
from django.contrib import messages
from comment.models import Comment
from decimal import Decimal
# Create your views here.
@login_required
def add_product(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    if request.method == 'POST':
        #store = Store.objects.filter(slug=store_slug)
        new_product_form = addForm(files=request.FILES, data=request.POST)
        if new_product_form.is_valid():
            new_product = new_product_form.save(commit=False)
            cd = new_product_form.cleaned_data
            if Product.objects.filter(name=cd['name'], store=store).exists():
                messages.error(request, 'the same product name')
                return render(request, 'product/add_product.html', {'form':new_product_form, 'store':store})
            else:
                new_product.slug = new_product.name
                new_product.store = store
                new_product.old_price = new_product.price
                new_product.save()
                messages.success(request, 'add successfully')
                return render(request, 'index_store.html', {'store':store})
    else:
        form = addForm()
        return render(request, 'product/add_product.html', {'form':form, 'store':store})

@login_required
def delete_product(request, store_slug, product_id):
    product = get_object_or_404(Product, id=product_id)
    store = Store.objects.filter(slug=store_slug)
    if request.method == 'POST':
        if product:
            Product.objects.get(id=product_id).delete()
            messages.success(request, 'delete successfully')
            return render(request, 'index_store.html',{'store':store})
        else:
            messages.error(request, 'the product has been delete')
            return render(request, 'index_store.html',{'store':store})
    return render(request, 'product/delete_product.html', {'product':product})

@login_required
def edit_product(request, store_slug, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        new_product_form = editForm(files=request.FILES, data=request.POST, instance=product)
        new_discount_form = discountProductForm(data=request.POST)
        if new_product_form.is_valid() and new_discount_form.is_valid():
            new_product_form.save()
            cd_discount = new_discount_form.cleaned_data
            if cd_discount['discount'] != '10':
                product.price = float(Decimal(product.old_price))*float(Decimal(cd_discount['discount']))/10
                product.discounted = True
            else:
                product.discounted = False
            product.save()
            messages.success(request, 'Product updated successfully')
            return render(request, 'product/edit_product.html',{'form':new_product_form,'discount_form':new_discount_form,'product':product})
        else:
            messages.error(request, 'Error updating your store')
            return render(request, 'product/edit_product.html',{'form':new_product_form,'discount_form':new_discount_form,'product':product})
    else:
        new_product_form = editForm(instance=product)
        new_discount_form = discountProductForm()
    return render(request, 'product/edit_product.html',{'form':new_product_form,'discount_form':new_discount_form,'product':product})

def list_product(request, store_slug):
    if request.method == 'POST':
        form = searchProductForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            store = get_object_or_404(Store, slug=store_slug)
            if cd['name'] == '':
                products = Product.objects.filter(store=store, available=True).all()
            else:
                products = Product.objects.filter(store=store, name=cd['name'], available=True).all()
    else:
        form = searchProductForm()
        store = get_object_or_404(Store, slug=store_slug)
        products = Product.objects.filter(store=store, available=True).all()
    return render(request,'product/list_product.html', {'form':form, 'store':store, 'products':products})

def detail_product(request, store_slug, product_id):
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product = product)
    add_cart_form = CartAddProductForm()
    if product.user_want.filter(id=request.user.id).exists():
        user_want = True
    else:
        user_want = False
    return render(request,'product/detail_product.html', {'store':store, 'product':product,
                                                            'add_cart_form': add_cart_form,'comments':comments,
                                                            'user_want':user_want})
def search_index(request):
    if request.method == 'POST':
        form = searchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['searchType'] == '1':
                products = Product.objects.filter(name = cd['name']).all()
                return render(request, 'search_index.html', {'form':form, 'products':products})
            else:
                stores = Store.objects.filter(name = cd['name']).all()
                return render(request, 'search_index.html', {'form':form, 'stores':stores})
    else:
        form = searchForm()
    return render(request, 'search_index.html', {'form':form})

def add_user_want(request, store_slug, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.user_want.add(request.user)
    return redirect('detail_product', store_slug, product_id)

def delete_user_want(request, store_slug, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.user_want.remove(request.user)
    return redirect('detail_product', store_slug, product_id)

def index_product_want(request):
    products = request.user.product_want.all()
    return render(request,'index_product_want.html', {'products':products})
