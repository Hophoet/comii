from django.contrib import admin
from .models import Item, Cart, OrderItem, Cart, Order, BillingAddress, Payment

# Register your models here.
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(BillingAddress)
admin.site.register(Payment)
# admin.site.register()