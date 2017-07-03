from django.db import models
from django.conf import settings
# Create your models here.
class Store(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='store')
    name = models.CharField(max_length=10)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    photo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
