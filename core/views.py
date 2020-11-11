import time 
import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from  django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required

#
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (Item, OrderItem, Cart, User, 
Order, BillingAddress, Payment)
from .forms import CheckoutForm

#stripe
import stripe

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
    template_name = 'item_detail.html'
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
        #begin with the order

    order, order_created = Order.objects.get_or_create(
                user=request.user,
                ordered=False,
                cart=cart

            )
    if order_created:
        print('ORDER CREATION')
    else:
        print('ODER ALRAIDY EXISTS')

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
            # print(cart.get_order_items_query())
            return render(self.request, 'order_summary.html', context)

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

            
            return render(self.request, 'checkout.html', context)
        return redirect('core:home')
    
    def post(self, *args, **kwargs):
        """ post request method """
        cart, cart_created = Cart.objects.get_or_create(
        user=self.request.user,
        ordered=False
        )
        if not cart_created:
            order, order_created = Order.objects.get_or_create(
                    user=self.request.user,
                    ordered=False,
                    cart=cart

            )

            try:
                
                checkout_form = CheckoutForm(self.request.POST or None)
                #check the validation of the checkout form
                if checkout_form.is_valid():
                    user = self.request.user
                    street_address = checkout_form.cleaned_data['street_address']
                    apartment_address = checkout_form.cleaned_data['apartment_address']
                    country = checkout_form.cleaned_data['country']
                    zip_code = checkout_form.cleaned_data['zip_code']
                    payment_option = checkout_form.cleaned_data['payment_option']
                    same_billing_address = checkout_form.cleaned_data['same_billing_address']
                    save_info = checkout_form.cleaned_data['save_info']
                    # print(user, street_address, apartment_address, country, zip_code, payment_option, same_billing_address, save_info, sep='\n')
                    billing_address = BillingAddress.objects.create(
                        user=user,
                        street_address=street_address,
                        apartment_address=apartment_address,
                        country=country,
                        zip_code = zip_code,
                    )
                    order.billing_address = billing_address
                    order.save()
                    if payment_option == 'S':
                        return redirect('core:stripe_payment')

            except Exception as error:
                print('ERROR', error)
                return redirect('core:checkout')
            return redirect('core:checkout')

        return redirect('core:home')




    
class StripePaymentView(LoginRequiredMixin, View):
    """ stripe option payment controller """
    def get(self, *args, **kwargs):
        """ get request method """
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )
        context = {'cart':cart}
        return render(self.request, 'stripe_payment.html', context)

    def post(self, *args, **kwargs):
        """ post  request method """
        # import pdb; pdb.set_trace()
        stripe_token = self.request.POST.get('stripeToken')
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )

        stripe.api_key = "key"
    

        data = self.request.POST
        if self.request.POST.get('card-code'):
            print('CART CODE', self.request.POST.get('card-code'))
            order, order_created = Order.objects.get_or_create(
                user=self.request.user,
                ordered=False,
                cart=cart
            )
            if order_created:
                pass
                # print('NEW CREATION')

            else:
                # print('ORDER ALRADY EXISTS')

                #payment stripe charge test id
                stripe_charge_id = 283
                #create payment
                payment = Payment.objects.create(
                    stripe_charge_id=stripe_charge_id,
                    user=self.request.user,
                    amounts=order.cart.get_total_price()
                )
                #update order
                order.payment = payment
                order.ordered_date = datetime.datetime.now()
                order.ordered = True
                order.save()
                order.cart.complete_order()
                messages.info(self.request, f'Order done successfully!!')
                return redirect('core:home')
                
                


        
        # print('DATA',data, stripe_token)
        return redirect('core:stripe_payment')

        
def success_payment(request):
    context = {}
    return render(request, 'success_payment.html', context)
    