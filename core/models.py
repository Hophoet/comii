from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Users model
User = settings.AUTH_USER_MODEL
#items categories
ITEMS_CATEGORIES = (
    ('S', 'Shirt'),
    ('OW', 'Out Wear'),
    ('SH', 'Shoe'),
    ('NT', 'New Tech'),
)
#items model
class Item(models.Model):
    title = models.CharField(verbose_name='title', max_length=100)
    price =  models.IntegerField(verbose_name='price')
    discount_price = models.IntegerField(verbose_name='discount price', null=True, blank=True)
    # image = models.ImageField(verbose_name='image', null=True, blank=True)
    image = models.CharField(verbose_name='image', max_length=1000)
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


  
#coupon request model
class Coupon(models.Model):
    code = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        """ coupon instace print method """
        return self.code



#shoping carts models
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
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
        if self.coupon:
            total_price -= self.coupon.amount
        return total_price

    def complete_order(self):
        # self.ordered = True
        for order_item in self.orderitem_set.get_queryset():
            order_item.ordered = True
            order_item.save()
        self.ordered = True
        self.save()
     
    def __str__(self):
        return f'{self.user.username} {self.orderitem_set.count()}'

#order items model(intermediaire between item and the shoping cart)
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)

    def update_item_quantity(self):
        """ method to  update the item related to the orderitem """
        self.item.quantity -= self.quantity
        self.item.save()

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


#Billing address model 
class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

#Payment model
class Payment(models.Model):
    """ Payment models """
    phone_number = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """" models print show """
        return self.user.username

#Order model 
class Order(models.Model):
    """ order management model """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField( null=True, blank=True)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey(BillingAddress, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    delivered = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)


    def __str__(self):
        """ order printer """
        return self.user.username





