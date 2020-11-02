from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Users model
User = settings.AUTH_USER_MODEL
#items categories
ITEMS_CATEGORIES = (
    ('S', 'Shirt'),
    ('OW', 'Out Wear')
)
#items model
class Item(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    price =  models.IntegerField(verbose_name='price')
    discount_price = models.IntegerField(verbose_name='discount price', null=True, blank=True)
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    category = models.CharField(verbose_name='category', choices=ITEMS_CATEGORIES, max_length=2)
    description = models.TextField(verbose_name='description')
    quantity = models.IntegerField(verbose_name='quantity')


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'core:item_detail',
            kwargs={
                'pk':self.id
            }
        )

    def get_add_to_cart_url(self):
        return reverse(
            'core:add_to_cart',
            kwargs={
                'id':self.id
            }
        )

    def get_remove_from_cart_url(self):
        return reverse(
            'core:remove_from_cart',
            kwargs={
                'id':self.id
            }
        )

#shoping carts models
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    #cart items count getter
    def get_items_count(self):
        order_items = self.orderitem_set.get_queryset()
        count = order_items.count()
        return count
    
    #cart query order items getter
    def get_order_items_query(self):
        order_items_query = self.orderitem_set.get_queryset()
        return order_items_query

    def get_total_price(self):
        order_items = self.orderitem_set.get_queryset()
        total_price = 0

        for order_item in order_items:
            total_price += order_item.get_final_price() * order_item.quantity
        return total_price

    def __str__(self):
        return f'{self.user.username} {self.orderitem_set.count()}'

#order items model(intermediaire between item and the shoping cart)
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)

    def get_amount_saved(self):
        if self.item.discount_price:
            saved_amount = self.item.price - self.item.discount_price
            return saved_amount
        return 0

    def get_total_order_item_price(self):
        total_order_item_price = self.get_final_price() * self.quantity
        return total_order_item_price


    def get_final_price(self):
        if self.item.discount_price:
            return self.item.discount_price
        return self.item.price

    def add_single_order_item_to_cart(self):
        return reverse(
            'core:add_single_order_item_to_cart',
            kwargs={
                'id':self.id
            }
        )

    def remove_single_order_item_from_cart(self):
        return reverse(
            'core:remove_single_order_item_from_cart',
            kwargs={
                'id':self.id
            }
        )


    def __str__(self):
        return self.item.title
