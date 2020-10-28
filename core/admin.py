from django.contrib import admin
from .models import Item, Cart, OrderItem, Cart 

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(OrderItem)
# admin.site.register()