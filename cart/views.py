from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from store.models import Product
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.
@require_POST
def add_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_cart(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('index_cart')

def remove_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_cart(product=product)
    return redirect('index_cart')

def index_cart(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'index_cart.html', {'cart': cart})
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'index_cart.html', {'cart': cart})
