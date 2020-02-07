from django.urls import path
from .views import (home, stripe_config, create_checkout_session, SuccessView, CancelledView)
#application name
app_name = 'stripetest'

urlpatterns = [
    path('', home, name='home'),
    path('config/', stripe_config ),
    path('create-checkout-session/', create_checkout_session), # new
    path('success/', SuccessView.as_view()), # new
    path('cancelled/', CancelledView.as_view()), # new

]