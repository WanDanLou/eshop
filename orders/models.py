from django.db import models
from django.core.urlresolvers import reverse
from store.models import Product,Store
from django.conf import settings
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='order_user')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    message = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    wait_recieved = models.BooleanField(default=False)
    class Meta:
        ordering = ('-created', )
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    def get_detail_url(self):
        return reverse('detail_order', args=[self.id])

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orderItem_user')
    order = models.ForeignKey(Order, related_name='items')
    product = models.ForeignKey(Product, related_name='orderItems_product')
    store = models.ForeignKey(Store, related_name='orderItems_store')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    def get_cost(self):
        return self.price * self.quantity
