from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .product_forms import addForm, editForm, searchForm, searchProductForm, discountProductForm, categoryForm
from cart.forms import CartAddProductForm
from .models import Store, Product
from account.models import Profile
from django.contrib import messages
from comment.models import Comment
from decimal import Decimal
# Create your views here.
CATEGORY_KEY ={'1':'不知道怎么分类', '2':'攻击' , '3':'法术', '4':'防御', '5':'移动', '6':'打野及消耗品'}
@login_required
def add_product(request, store_slug):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    if store.user.id != request.user.id:
        return redirect('index')
    if request.method == 'POST':
        #store = Store.objects.filter(slug=store_slug)
        new_product_form = addForm(files=request.FILES, data=request.POST)
        new_category_form = categoryForm(data=request.POST)
        if new_product_form.is_valid() and new_category_form.is_valid():
            new_product = new_product_form.save(commit=False)
            cd = new_product_form.cleaned_data
            if Product.objects.filter(name=cd['name'], store=store).exists():
                messages.error(request, 'the same product name')
                return render(request, 'product/add_product.html', {'form':new_product_form,
                                                                    'category_form':new_category_form, 'store':store})
            elif Decimal(cd['price']) <= 0:
                messages.error(request, '价格非正')
                return render(request, 'product/add_product.html', {'form':new_product_form,
                                                                    'category_form':new_category_form, 'store':store})
            else:
                cd_category = new_category_form.cleaned_data
                new_product.category = CATEGORY_KEY[cd_category['category']]
                new_product.slug = new_product.name
                new_product.store = store
                new_product.old_price = new_product.price
                new_product.save()
                messages.success(request, 'add successfully')
                return redirect('index')
    else:
        form = addForm()
        new_category_form = categoryForm()
        return render(request, 'product/add_product.html', {'form':form,
                                                            'category_form':new_category_form, 'store':store})

@login_required
def delete_product(request, store_slug, product_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    if store.user.id != request.user.id:
        return redirect('index')
    product = get_object_or_404(Product, id=product_id)
    if product.store.id != store.id:
        return redirect('index')
    if request.method == 'POST':
        if product:
            Product.objects.get(id=product_id).delete()
            messages.success(request, 'delete successfully')
            return render(request, 'index_orderItem.html',{'store':store})
        else:
            messages.error(request, 'the product has been delete')
            return render(request, 'index_store.html',{'store':store})
    return render(request, 'product/delete_product.html', {'product':product})

@login_required
def edit_product(request, store_slug, product_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    if store.user.id != request.user.id:
        return redirect('index')
    product = get_object_or_404(Product, id=product_id)
    if product.store.id != store.id:
        return redirect('index')
    if request.method == 'POST':
        new_product_form = editForm(files=request.FILES, data=request.POST, instance=product)
        new_discount_form = discountProductForm(data=request.POST)
        new_category_form = categoryForm(data=request.POST)
        if new_product_form.is_valid() and new_discount_form.is_valid() and new_category_form.is_valid():
            cd = new_product_form.cleaned_data
            if Product.objects.filter(name=cd['name'], store=store).exclude(id=product_id).exists():
                messages.error(request, 'name has existed')
            elif Decimal(cd['old_price']) <= 0:
                messages.error(request, '价格非正')
            else:
                new_product_form.save()
                cd_discount = new_discount_form.cleaned_data
                cd_category = new_category_form.cleaned_data
                product.category = CATEGORY_KEY[cd_category['category']]
                if cd_discount['discount'] != '10':
                    product.price = float(Decimal(product.old_price))*float(Decimal(cd_discount['discount']))/10
                    product.discounted = True
                else:
                    product.price = product.old_price
                    product.discounted = False
                product.save()
                messages.success(request, 'Product updated successfully')
            return redirect('edit_product', store_slug, product_id)
        else:
            messages.error(request, 'Error updating your store')
        return render(request, 'product/edit_product.html',{'form':new_product_form,'category_form':new_category_form,
                                                                'discount_form':new_discount_form,'product':product})
    else:
        new_product_form = editForm(instance=product)
        new_discount_form = discountProductForm()
        new_category_form = categoryForm()
    return render(request, 'product/edit_product.html',{'form':new_product_form,'category_form':new_category_form,
                                                        'discount_form':new_discount_form,'product':product})

def list_product(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
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
        form = searchProductForm(data=request.POST)
        store = get_object_or_404(Store, slug=store_slug)
        products = Product.objects.filter(store=store, available=True).all()
    if store.category_show != 0:
        products = products.filter(category=CATEGORY_KEY[str(store.category_show)]).all()
    order_price = "-price"
    if store.order_price:
        order_price = "price"
    if store.sort_price:
        order_price = "sort_order"
    order_volume = "-volume"
    if store.order_volume:
        order_volume = "volume"
    if store.sort_volume:
        order_volume = "sort_order"
    order_created = "-created"
    if store.order_created:
        order_created = "created"
    if store.sort_created:
        order_created = "sort_order"
    order_name = "-name"
    if store.order_name:
        order_name = "name"
    if store.sort_name:
        order_name = "sort_order"
    products = products.order_by(order_created, order_name, order_volume, order_price )
    return render(request,'product/list_product.html', {'form':form, 'store':store, 'products':products})

def detail_product(request, store_slug, product_id):
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, id=product_id)
    comments = Comment.objects.filter(product = product)
    add_cart_form = CartAddProductForm()
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        if not user.product_visit.filter(id=product.id).exists():
            user.product_visit.add(product)
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
                if cd['name']== '':
                    products = Product.objects.all()
                else:
                    products = Product.objects.filter(name = cd['name']).all()
                flag = ''
                if cd['orderType'] == '1':
                    flag = '-'
                if cd['sortType'] == '0':
                    products = products.order_by(flag + "created")
                if cd['sortType'] == '1':
                    products = products.order_by(flag + "price")
                if cd['sortType'] == '2':
                    products = products.order_by(flag + "volume")
                if cd['filterType'] != '0':
                    products = products.filter(category=CATEGORY_KEY[str(cd['filterType'])]).all()
                return render(request, 'search_index.html', {'form':form, 'products':products})
            else:
                stores = Store.objects.filter(name = cd['name']).all()
                return render(request, 'search_index.html', {'form':form, 'stores':stores})
    else:
        form = searchForm()
    return render(request, 'search_index.html', {'form':form})

@login_required
def add_user_want(request, store_slug, product_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, id=product_id)
    if product.store.id != store.id:
        return redirect('index')
    product.user_want.add(request.user)
    return redirect('detail_product', store_slug, product_id)
@login_required
def delete_user_want(request, store_slug, product_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    product = get_object_or_404(Product, id=product_id)
    if product.store.id != store.id:
        return redirect('index')
    product.user_want.remove(request.user)
    return redirect('detail_product', store_slug, product_id)
@login_required
def index_product_want(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    products = request.user.product_want.all()
    return render(request,'index_product_want.html', {'products':products})
@login_required
def index_product_visit(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    products = request.user.product_visit.all()
    products = products.order_by("name")
    return render(request,'index_product_visit.html', {'products':products})

def list_product_filter(request, store_slug, filter_type):
    store = get_object_or_404(Store, slug=store_slug)
    store.category_show = filter_type
    store.save()
    form = searchProductForm()
    return redirect('list_product', store_slug)

def reverse_bool(a):
    if a == False:
        return True
    else:
        return False
def order_product_created(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.order_created = reverse_bool(store.order_created)
    store.save()
    return redirect('list_product', store_slug)

def order_product_price(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.order_price = reverse_bool(store.order_price)
    store.save()
    return redirect('list_product', store_slug)

def order_product_name(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.order_name = reverse_bool(store.order_name)
    store.save()
    return redirect('list_product', store_slug)

def order_product_volume(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.order_volume = reverse_bool(store.order_volume)
    store.save()
    return redirect('list_product', store_slug)

def sort_product_created(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.sort_created = reverse_bool(store.sort_created)
    store.save()
    return redirect('list_product', store_slug)

def sort_product_price(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.sort_price = reverse_bool(store.sort_price)
    store.save()
    return redirect('list_product', store_slug)

def sort_product_name(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.sort_name = reverse_bool(store.sort_name)
    store.save()
    return redirect('list_product', store_slug)

def sort_product_volume(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    store.sort_volume = reverse_bool(store.sort_volume)
    store.save()
    return redirect('list_product', store_slug)
