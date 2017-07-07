from django.contrib import admin
from .models import Store, Product

# Register your models here.
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'photo', 'description')
admin.site.register(Store, StoreAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image', 'description')
admin.site.register(Product, ProductAdmin)
