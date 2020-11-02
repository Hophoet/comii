from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from  django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required

#
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Item, OrderItem, Cart, User
from .forms import CheckoutForm

# Create your views here.
class HomeView(ListView):
    """ Home page view """
    model = Item
    template_name = 'home.html'
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
        ordered=False
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
        ordered=False
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

    return redirect('core:item_detail', pk=id)


@login_required
def add_single_order_item_to_cart(request, id):
    order_item = get_object_or_404(OrderItem, id=id)
    cart, cart_created = Cart.objects.get_or_create(
        user=request.user,
        ordered=False
    )
    
    cart_order_item_exists = order_item in  cart.orderitem_set.get_queryset()
    if cart_order_item_exists:
        new_quantity = order_item.quantity + 1
        set_posible = True if(order_item.item.quantity >= new_quantity) else False
        if set_posible:
            # print('POSSIBLE', order_item.item.quantity, order_item.quantity)
            order_item.quantity = new_quantity
            order_item.save()
            messages.info(request, 'item updated')
        else:
            # print('NOT POSSIBLE', order_item.item.quantity, order_item.quantity)

            messages.info(request, 'you reach the item high quantity')
        return redirect('core:cart')

@login_required
def remove_single_order_item_from_cart(request, id):
    order_item = get_object_or_404(OrderItem, id=id)
    cart, cart_created = Cart.objects.get_or_create(
        user=request.user,
        ordered=False
    )
    
    new_quantity = order_item.quantity - 1
    remove_order_item_from_cart = True if(order_item.quantity == 1) else False
    if remove_order_item_from_cart:
        cart.orderitem_set.remove(order_item)
        messages.info(request, 'item removed')
    else:
        # print('POSSIBLE', order_item.item.quantity, order_item.quantity)
        order_item.quantity = new_quantity
        order_item.save()
        messages.info(request, 'item update')
    return redirect('core:cart')
    



class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        #geting of the order_item, or creation if not exists
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )
        if not cart_created:
            context = {
                'cart': cart
            }
            print(cart.get_order_items_query())
            return render(self.request, 'core/cart.html', context)

        return redirect('core:home')

    
class CheckoutView(LoginRequiredMixin, View):
    """ Checkout view """
    def get(self, *args, **kwargs):
        """ get request method """
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            ordered=False,
        )
        
        if not cart_created:
            checkout_form = CheckoutForm()
            context =  {
                'cart':cart,
                'checkout_form':checkout_form
            }

            
            return render(self.request, 'core/checkout.html', context)
        return redirect('core:home')