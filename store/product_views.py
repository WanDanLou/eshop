from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .product_forms import addForm, editForm
from cart.forms import CartAddProductForm
from .models import Store, Product
from account.models import Profile
from django.contrib import messages
# Create your views here.
@login_required
def add_product(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    if request.method == 'POST':
        #store = Store.objects.filter(slug=store_slug)
        new_product_form = addForm(request.POST)
        if new_product_form.is_valid():
            new_product = new_product_form.save(commit=False)
            cd = new_product_form.cleaned_data
            if Product.objects.filter(name=cd['name'], store=store).exists():
                messages.error(request, 'the same product name')
                return render(request, 'product/add_product.html', {'form':new_product_form, 'store':store})
            else:
                new_product.slug = new_product.name
                new_product.store = store
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
        new_product_form = editForm(instance=product,data=request.POST)
        if new_product_form.is_valid():
            new_product_form.save()
            messages.success(request, 'Product updated successfully')
            return render(request, 'product/edit_product.html',{'form':new_product_form,'product':product})
        else:
            messages.error(request, 'Error updating your store')
            return render(request, 'product/edit_product.html',{'form':new_product_form,'product':product})
    else:
        new_product_form = editForm(instance=product)
    return render(request, 'product/edit_product.html',{'form':new_product_form,'product':product})

def list_product(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    products = Product.objects.filter(store=store, available=True).all()
    return render(request,'product/list_product.html', {'store':store, 'products':products})

def detail_product(request, store_slug, product_id):
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, id=product_id)
    add_cart_form = CartAddProductForm()
    return render(request,'product/detail_product.html', {'store':store, 'product':product, 'add_cart_form': add_cart_form})
