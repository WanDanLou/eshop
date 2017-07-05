from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from .models import Order, OrderItem
from django.contrib import messages
from cart.cart import Cart
# Create your views here.
@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity'])
            cart.clear()
            order.save()
            orders = Order.objects.filter(user=request.user).all()
            return render(request, 'index_order.html', {'orders': orders})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form})

@login_required
def index_order(request):
    orders = Order.objects.filter(user=request.user).all()
    return render(request, 'index_order.html', {'orders': orders})

@login_required
def detail_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderItems = OrderItem.objects.filter(order=order)
    return render(request, 'orders/detail_order.html', {'order': order, 'orderItems':orderItems})

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/pay_order.html', {'order': order})

@login_required
def pay_order_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.profile.money > order.get_total_cost():
        request.user.profile.money = request.user.profile.money - order.get_total_cost()
        request.user.profile.save()
        for item in order.items.all():
            store = item.product.store
            store.money = store.money + item.get_cost()
            store.save()
        messages.success(request, 'pay successfully')
        order.paid = True
        order.save()
    else:
        messages.error(request, 'money not enough')
    return redirect('index_order')

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/delete_order.html', {'order': order})

@login_required
def delete_order_done(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    messages.success(request, 'delete successfully')
    for item in order.items.all():
        item.delete()
    order.delete()
    return redirect('index_order')
