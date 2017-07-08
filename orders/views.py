from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm, searchOrderForm
from .models import Order, OrderItem
from comment.models import Comment
from store.models import Store, Product
from django.contrib import messages
from cart.cart import Cart
from comment.forms import CommentForm,ReplyForm
# Create your views here.
@login_required
def create_order(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            flag = False
            for item in cart:
                flag = True
                OrderItem.objects.create(store=item['product'].store, order=order,user=request.user,product=item['product'], price=item['price'], quantity=item['quantity'])
            if flag == False:
                messages.error(request, "订单为空")
                return redirect('create_order')
            cart.clear()
            orders = Order.objects.filter(user=request.user).all()
            return render(request, 'index_order.html', {'orders': orders})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/create_order.html', {'cart': cart, 'form': form})

@login_required
def index_order(request):
    user = request.user
    if user.is_authenticated and user.profile.usertype :
        return redirect('index')
    orders = Order.objects.filter(user=request.user).all()
    if request.method == 'POST':
        form = searchOrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['paidType'] == '1':
                orders = orders.filter(paid=True).all()
            elif cd['paidType'] == '2':
                orders = orders.filter(paid=False).all()
            if cd['finishedType'] == '1':
                orders = orders.filter(finished=True).all()
            elif cd['finishedType'] == '2':
                orders = orders.filter(finished=False).all()
            if cd['wait_recievedType'] == '1':
                orders = orders.filter(wait_recieved=True).all()
            elif cd['wait_recievedType'] == '2':
                orders = orders.filter(wait_recieved=False).all()
            if cd['deletedType'] == '1':
                orders = orders.filter(deleted=True).all()
            else:
                orders = orders.filter(deleted=False).all()
    else:
        form = searchOrderForm()
    return render(request, 'index_order.html', {'form':form,'orders': orders})

@login_required
def detail_order(request, order_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.user.id:
        return redirect('index')
    orderItems = OrderItem.objects.filter(order=order).all()
    return render(request, 'orders/detail_order.html', {'order': order, 'orderItems':orderItems})

@login_required
def pay_order(request, order_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.user.id:
        return redirect('index')
    return render(request, 'orders/pay_order.html', {'order': order})

@login_required
def pay_order_done(request, order_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.user.id:
        return redirect('index')
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
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.user.id:
        return redirect('index')
    return render(request, 'orders/delete_order.html', {'order': order})

@login_required
def delete_order_done(request, order_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    order = get_object_or_404(Order, id=order_id)
    if order.user.id != request.user.id:
        return redirect('index')
    messages.success(request, 'delete successfully')
    if order.deleted == False:
        order.deleted = True
    else:
        order.deleted = False
    order.save()
    return redirect('index_order')

@login_required
def return_item(request, orderItem_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.user.id != request.user.id:
        return redirect('index')
    orderItem.wait_returned = True
    orderItem.save()
    return redirect('index_order')

@login_required
def return_item_done(request, orderItem_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
    orderItem.returned = True
    orderItem.wait_returned = False
    orderItem.save()
    store = orderItem.product.store
    store.money = store.money - orderItem.get_cost()
    store.save()
    profile = orderItem.user.profile
    profile.money = profile.money +  orderItem.get_cost()
    profile.save()
    return redirect('index_orderItem', store.slug)

@login_required
def index_orderItem(request, store_slug):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    store = get_object_or_404(Store, slug=store_slug)
    if store.user.id != request.user.id:
        return redirect('index')
    orderItems = OrderItem.objects.filter(store=store, paid=True).all()
    return render(request,'index_orderItem.html', {'orderItems':orderItems})

@login_required
def deliver_item(request, orderItem_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
    order = orderItem.order
    return render(request,'orderItems/deliver_orderItem.html', {'orderItem':orderItem, 'order':order})

@login_required
def detail_item(request, orderItem_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
    order = orderItem.order
    return render(request,'orderItems/detail_orderItem.html', {'orderItem':orderItem, 'order':order})

@login_required
def deliver_item_done(request, orderItem_id):
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
    orderItem.delivered = True
    orderItem.save()
    order = orderItem.order
    order.wait_recieved = True
    order.save()
    return redirect('index_orderItem',request.user.store.slug)

@login_required
def recieve_item(request, orderItem_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.user.id != request.user.id:
        return redirect('index')
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
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.user.id != request.user.id:
        return redirect('index')
    form = CommentForm(request.POST)
    if form.is_valid():
        orderItem.commented = True
        product = orderItem.product
        cd = form.cleaned_data
        comment = Comment()
        comment.orderitem = orderItem
        comment.product = product
        comment.author = request.user.profile
        comment.grade = cd['grade']
        comment.name = cd['name']
        comment.body = cd['body']
        orderItem.save()
        comment.save()
        messages.info(request, '评论成功 ')
        return redirect('index_order')
    else:
        messages.warning(request, '评论失败')
        return render(request, 'orders/comment_item.html', {'form': form,'orderItem':orderItem})

@login_required
def revision_comment(request, orderItem_id):
    user = request.user
    if user.is_authenticated and user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.user.id != request.user.id:
        return redirect('index')
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
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
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
    user = request.user
    if user.is_authenticated and not user.profile.usertype:
        return redirect('index')
    orderItem = get_object_or_404(OrderItem, id=orderItem_id)
    if orderItem.store.user.id != request.user.id:
        return redirect('index')
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
