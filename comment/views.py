from django.shortcuts import render
from .models import Comment
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
@login_required
@require_Product
def create_comment(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.product = product
        comment.save()
        messages.info(request, '评论成功 '.format(post.title))
    else:
        messages.warning(request, '评论失败')
    return return render(request, 'comment/create_comment.html', {'form': form})
