from django.db import models
from django.conf import settings
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='images/%Y/%m/%d',blank=True)
    age = models.PositiveIntegerField(null=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
