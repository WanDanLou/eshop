from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.core.urlresolvers import reverse
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    age = models.PositiveIntegerField(null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    usertype = models.BooleanField(default=False) # True is user

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='commodity')
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name', )
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])
