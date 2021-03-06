from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='store')
    name = models.CharField(max_length=10)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    photo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    money = models.PositiveIntegerField(default=1000)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    category_show = models.PositiveIntegerField(default=0)
    sort_created = models.BooleanField(default=False)#false 排
    sort_price = models.BooleanField(default=False)
    sort_name = models.BooleanField(default=False)
    sort_volume = models.BooleanField(default=False)
    order_created = models.BooleanField(default=False)#false 是从低到高
    order_price = models.BooleanField(default=False)
    order_name = models.BooleanField(default=False)
    order_volume = models.BooleanField(default=False)
    class Meta:
        ordering=['-created']
    def get_index_store_url(self):
        return reverse('index_store', args=[self.slug])
    def get_add_product_url(self):
        return reverse('add_product', args=[self.slug])
    def get_list_product_url(self):
        self.category_show = 0
        self.save()
        return reverse('list_product', args=[self.slug])
class Product(models.Model):
    store = models.ForeignKey(Store, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=200, default='不知道怎么分类')
    price = models.DecimalField(max_digits=100, decimal_places=2)
    old_price = models.DecimalField(max_digits=100, decimal_places=2)
    available = models.BooleanField(default=True)
    volume = models.PositiveIntegerField(default=0)
    sort_order =  models.PositiveIntegerField(default=0)#不排
    discounted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user_want = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_want')
    user_visit = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='product_visit')
    class Meta:
        ordering=['-created']
    def get_delete_product_url(self):
        return reverse('delete_product', args=[self.store.slug, self.id])
    def get_edit_product_url(self):
        return reverse('edit_product', args=[self.store.slug, self.id])
    def get_detail_product_url(self):
        return reverse('detail_product', args=[self.store.slug, self.id])
