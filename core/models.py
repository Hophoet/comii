from django.db import models
from django.conf import settings

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
    image = models.ImageField(verbose_name='image')
    category = models.CharField(verbose_name='category', choices=ITEMS_CATEGORIES, max_length=2)
    description = models.TextField(verbose_name='description')
    quantity = models.IntegerField(verbose_name='quantity')


    def __str__(self):
        return self.title

#shoping carts models
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)

    #cart items count getter
    def get_items_count(self):
        order_items = self.orderitem_set.get_queryset()
        count = order_items.count()
        return count
    def __str__(self):
        return f'{self.user.username} {self.orderitem_set.count()}'

#order items model(intermediaire between item and the shoping cart)
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.item.title
