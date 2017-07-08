from django.db import models
from store.models import Product
from account.models import Profile
from orders.models import OrderItem
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments')
    author = models.ForeignKey(Profile, related_name='comments')
    orderitem = models.OneToOneField(OrderItem)
    name = models.CharField(max_length=80)
    body = models.TextField()
    grade = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    reply = models.TextField()

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return 'Comment by {} on {}'.format(self.creater, self.product)
