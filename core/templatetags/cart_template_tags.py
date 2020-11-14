from django import template
from core.models import Cart
register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        carts_query = Cart.objects.filter(
            user=user,
            ordered=False
        )
        if carts_query.exists():
            cart = carts_query[0]
            print('CART', cart)
            count = cart.get_items_count()
            return count

        return 0
   
@register.filter
def cart_getter(user):
    if user.is_authenticated:
        cart, cart_created = Cart.objects.get_or_create(
        user=user,
        ordered=False
        )
        return  cart if(not cart_created) else None
    return None


@register.filter
def cart_contain_item(user, item):
    order_item, order_item_created = OrderItem.objects.get_or_create(
        item=item,
        user=user,
    )
    if not order_item_created:
        cart, cart_created = Cart.objects.get_or_create(
            user=request.user,
            ordered=False
        )
        
        cart_order_item_exists = order_item in  cart.orderitem_set.get_queryset()
        if cart_order_item_exists:
            return True
    return False

