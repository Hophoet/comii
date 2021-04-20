import time 
import datetime
from django.conf import settings
#
from django.core.mail import send_mail

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from  django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required

#
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import (Item, OrderItem, Cart, User, 
Order, BillingAddress, Payment, Coupon)
from .forms import CheckoutForm, CouponForm

#stripe
import stripe


def mailSender(subject, message, from_email, recipient_list):
    try:
        # send_mail(
        #     subject,
        #     message,
        #     from_email,
        #     recipient_list
        # )
        pass
    except Exception as error:
        print(error)

    else:
        print('message send successfully!')


# Create your views here.
class HomeView(ListView):
    """ Home page view """
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    # paginate_by = 4
    # ordering = 'title'

    def get_queryset(self, *args, **kwargs):
        """ queryset getter """
        items = Item.objects.all()
        return items




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
    if(item.quantity <= 0):
        messages.info(request, f'Ce produit est fini en stock.')
        return redirect('core:item_detail', pk=id)
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
        order_item.quantity = 1
        order_item.save()
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
            coupon_form = CouponForm()
            context =  {
                'cart':cart,
                'checkout_form':checkout_form,
                'coupon_form':coupon_form
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
                    # phone number for flooz payment for payment
                    phone_number = checkout_form.cleaned_data['phone_number']
                    billing_address = BillingAddress.objects.create(
                        user=user,
                        street_address=street_address,
                        apartment_address=apartment_address,
                        country=country,
                        zip_code = zip_code,
                    )
                    order.billing_address = billing_address
                    order.save()

            except Exception as error:
                return redirect('core:checkout')
            messages.info(self.request, f'order successfully')
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
        coupon_form = CouponForm()
        context = {'cart':cart, 'coupon_form': coupon_form}
        return render(self.request, 'stripe_payment.html', context)

    def post(self, *args, **kwargs):
        """ post  request method """
        # import pdb; pdb.set_trace()
        stripe_token = self.request.POST.get('stripeToken')
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            ordered=False
        )

        stripe.api_key = settings.STRIPE_SECRET_KEY
    

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
                #stripe charging
                test_stripe_token = '8JD894'
                amount = int(order.cart.get_total_price() * 100)
                
                #Stripe request 
                # mailSender('order', 'your order is ordered successfully', 'hophoet@gmail.com' ['test@gmail.com'])

                try:

                    charge = stripe.Charge.create(
                        amount=amount,
                        currency='usd',
                        source=self.request.POST.get('card-code')
                    )
                except stripe.error.CardError as error:
                    body = error.json_body
                    error = body.get('error', {})
                    messages.error(self.request, f'{error.get("message")}')
                except stripe.error.RateLimitError as error:
                    body = error.json_body
                    error = body.get('error', {})
                    messages.error(self.request, f'{error.get("message")}')
                except stripe.error.InvalidRequestError as error:
                    body = error.json_body
                    error = body.get('error', {})
                    messages.error(self.request, f'{error.get("message")}')
                except stripe.error.AuthenticationError as error:
                    body = error.json_body
                    error = body.get('error', {})
                    messages.error(self.request, f'{error.get("message")}')
                except stripe.error.APIConnectionError as error:
                    body = error.json_body
                    print('BODY', body)
                    # error = body.get('error', {})
                    messages.error(self.request, f'{"connexion error"}')
                except stripe.error.StripeError as error:
                    body = error.json_body
                    error = body.get('error', {})
                    messages.error(self.request, f'{error.get("message")}')
                except Exception as error:
                    messages.error(self.request, f'{error}')
                else:
                    print('Stripe TRYCATCH else')
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

        

class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)

        if form.is_valid():

            # order getting try condition
            try:
                code = form.cleaned_data.get('code')
                order, order_created = Order.objects.get_or_create(
                    user=self.request.user,
                    ordered=False
                )
                cart = order.cart
                #coupon getting try
                try:
                    coupon = Coupon.objects.get(code=code)
                except ObjectDoesNotExist:
                    messages.info(self.request, 'This coupon does not exist')
                    return redirect('core:checkout')
                #check if the current coupon not already added
                if(cart.coupon and cart.coupon.code == code):
                    #add info messages for the existing for the same coupon
                    messages.info(self.request, 'This coupon is already added')
                    return redirect('core:checkout')
                cart.coupon = coupon
                cart.save()
                messages.success(self.request, 'Coupon successfully added')
                return redirect('core:checkout')
            except ObjectDoesNotExist:
                messages.info(self.request, "You don't have an active order")
                return redirect('core:checkout')

