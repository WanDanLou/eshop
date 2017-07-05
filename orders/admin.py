from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'postal_code', 'message')
admin.site.register(Order, OrderAdmin)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('user', 'product','store','paid','price', 'quantity')
admin.site.register(OrderItem, OrderItemsAdmin)
