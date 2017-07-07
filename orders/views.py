from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm
from .models import Order, OrderItem
from comment.models import Comment
from store.models import Store, Product
from django.contrib import messages
from cart.cart import Cart
from comment.forms import CommentForm
# Create your views here.
@login_required
def create_order(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(store=item['product'].store, order=order,user=request.user,product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            orders = Order.objects.filter(user=request.user).all()
            return render(request, 'index_order.html', {'orders': orders})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form})

@login_required
def index_order(request):
    orders = Order.objects.filter(user=request.user, deleted=False).all()
    return render(request, 'index_order.html', {'orders': orders})

@login_required
def detail_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    orderItems = OrderItem.objects.filter(order=order).all()
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
        orderItems = OrderItem.objects.filter(order=order).all()
        for item in orderItems:
            item.paid = True
            item.save()
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
    order.deleted = True
    order.save()
    return redirect('index_order')
@login_required
def index_orderItem(request, store_slug):
    store = get_object_or_404(Store, slug=store_slug)
    orderItems = OrderItem.objects.filter(store=store, paid=True).all()
    return render(request,'index_orderItem.html', {'orderItems':orderItems})

@login_required
def deliver_item(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    order = orderItem.order
    return render(request,'orderItems/deliver_orderItem.html', {'orderItem':orderItem, 'order':order})

@login_required
def detail_item(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    order = orderItem.order
    return render(request,'orderItems/detail_orderItem.html', {'orderItem':orderItem, 'order':order})

@login_required
def deliver_item_done(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    orderItem.delivered = True
    orderItem.save()
    order = orderItem.order
    order.wait_recieved = True
    order.save()
    return redirect('index_orderItem',request.user.store.slug)

@login_required
def recieve_item(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    orderItem.recieved = True
    store = orderItem.store
    store.money = store.money + orderItem.get_cost()
    store.save()
    orderItem.save()
    order=orderItem.order
    if OrderItem.objects.filter(order=order, delivered=True, recieved=False).exists():
        order.wait_recieved = True
    else:
        order.wait_recieved = False
    if OrderItem.objects.filter(order=order, recieved=False).exists():
        order.finished = False
    else:
        order.finished = True
    order.save()
    return redirect('detail_order', orderItem.order.id)

@login_required
def make_comment(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if(request.method == 'POST'):
        form = CommentForm(request.POST)
        if form.is_valid():
            orderItem.commented = True
            product = orderItem.product
            cd = form.cleaned_data
            comment = Comment()
            comment.product = product
            comment.author = request.user.profile
            comment.grade = cd['grade']
            comment.name = request.user.username
            comment.body = cd['body']
            orderItem.save()
            comment.save()
            messages.info(request, '评论成功 ')
            return redirect('index_order')
        else:
            messages.warning(request, '评论失败')
            return render(request, 'orders/comment_item.html', {'form': form,'orderItem':orderItem})
    else:
        form = CommentForm()
        return render(request, 'orders/comment_item.html', {'form': form,'orderItem':orderItem})

@login_required
def revision_comment(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    comment = get_object_or_404(Comment, orderitem = orderItem)
    form = CommentForm(request.POST)
    if form.is_valid():
        product = orderItem.product
        cd = form.cleaned_data
        comment.grade = cd['grade']
        comment.name = cd['name']
        comment.body = cd['body']
        comment.save()
        messages.info(request, '修改成功 ')
        return redirect('index_order')
    else:
        messages.warning(request, '修改失败')
        return render(request, 'orders/revision_comment.html', {'form': form,'orderItem':orderItem})

@login_required
def reply_item(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    comment = get_object_or_404(Comment, orderitem = orderItem)
    form = ReplyForm(request.POST)
    if form.is_valid():
        orderItem.replied = True
        cd = form.cleaned_data
        comment.reply = cd['reply']
        comment.save()
        orderItem.save()
        messages.info(request, '回復成功 ')
        return redirect('index_orderItem',request.user.store.slug)
    else:
        messages.warning(request, '回復失敗')
        return render(request, 'orders/reply_item.html', {'form': form,'orderItem':orderItem, 'comment':comment})

@login_required
def revision_reply(request, orderItem_id):
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    comment = get_object_or_404(Comment, orderitem = orderItem)
    form = ReplyForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        comment.reply = cd['reply']
        comment.save()
        messages.info(request, '修改成功 ')
        return redirect('index_orderItem',request.user.store.slug)
    else:
        messages.warning(request, '修改失败')
        return render(request, 'orders/revision_reply.html', {'form': form,'orderItem':orderItem,'comment':comment})
