from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from  django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required

from .models import Item, OrderItem, Cart, User
# Create your views here.
def home(request):
    return render(request, 'core/index.html', {})


# Create your views here.
class HomeView(ListView):
    """ Home page view """
    model = Item
    template_name = 'core/index.html'
    context_object_name = 'items'
    # paginate_by = 4
    # ordering = 'title'



class ItemDetailView(DetailView):
    """ Item detail page view """
    model = Item
    template_name = 'core/item_detail.html'
    context_object_name = 'item'



@login_required
def add_to_cart(request, id):
    """ add to cart view method manager """
    #get of the item
    item = get_object_or_404(Item, id=id)
    #geting of the order_item, or creation if not exists
    order_item, order_item_created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
    )
    cart, cart_created = Cart.objects.get_or_create(
        user=request.user,
        ordered=False
    )
    
    cart_order_item_exists = order_item in  cart.orderitem_set.get_queryset()

    # print('CART ORDER ITEMS QUERYSET', dir(cart.orderitem_set), cart.orderitem_set.get_queryset(), cart_order_item_exists)
    if cart_order_item_exists:
        print('item alraidy added')
        messages.info(request, f'This item is alraidy add.')

    #     print(cart_order_items_queryset)
    else:
        cart.orderitem_set.add(order_item)
        print('item added successfully!')
        messages.info(request, f'This item({order_item.quantity}) was added to your cart!')

    # print('ORDER ITEM', order_item)
    # print('USER', request.user)
    # print('CART', cart, cart_created)
    # print('CART ORDERITEMS', cart.orderitem_set.all())
    #get of the order of the current user, and (not ordered)
    # order_queryset = Order.objects.filter(user=request.user, ordered=False)
    # #case: if the user has alrady an unordered order
    # if order_queryset.exists():
    #     #get of the order in the query set
    #     order = order_queryset[0]
    #     #check if the order item is in the order
    #     if order.items.filter(item__id=item.id).exists():
    #         #don't do nothing
    #         messages.info(request, f'This item is alraidy add.')
    #     #the item not in the cart
    #     else:
    #         messages.info(request, f'This item({order_item.quantity}) was added to your cart.')
    #         #add in the cart
    #         order.items.add(order_item)
    # else:
    #     #the user has not alrady an unordered order
    #     ordered_date = timezone.now()
    #     #creation of a new order
    #     order = Order.objects.create(
    #         user=request.user, ordered_date=ordered_date
    #     )
    #     #adding the current item to add in the cart
    #     order.items.add(order_item)
    #     messages.info(request, f'This item({order_item.quantity}) was added to your cart.')

    return redirect('core:item_detail', pk=id)



@login_required
def remove_from_cart(request, id):
    """ Remove item view controller """
     #get of the item
    item = get_object_or_404(Item, id=id)
    #geting of the order_item, or creation if not exists
    order_item, order_item_created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
    )
    cart, cart_created = Cart.objects.get_or_create(
        user=request.user,
        ordered=False
    )
    
    cart_order_item_exists = order_item in  cart.orderitem_set.get_queryset()

    if cart_order_item_exists:
        cart.orderitem_set.remove(order_item)
        messages.info(request, 'This item was removed form your cart')
    else:
        messages.info(request, 'This item was not in your cart')



    # order_queryset = Order.objects.filter(user=request.user, ordered=False)
    # #check if the orderqs exists
    # if order_queryset.exists():
    #     order = order_queryset[0]
    #     #check if the order item is in the order
    #     if order.items.filter(item__slug=item.slug).exists():
    #         order_item = OrderItem.objects.filter(
    #             item=item,
    #             user=request.user,
    #             ordered=False
    #         )[0]
    #         order.items.remove(order_item)
    #         order_item.delete()
    #         messages.info(request, 'This item was removed form your cart.')
    #     else:
    #         messages.info(request, 'This item was not in your cart.')
    #         return redirect('core:product', slug=slug)
    # else:
    #     messages.info(request, 'You do not have an order.')
    return redirect('core:item_detail', pk=id)



