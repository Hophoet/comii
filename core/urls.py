from django.urls import path
from . import views
#application name
app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('add-single-order-item-to-cart/<int:id>/', views.add_single_order_item_to_cart, name='add_single_order_item_to_cart' ),
    path('remove-single-order-item-from-cart/<int:id>/', views.remove_single_order_item_from_cart, name='remove_single_order_item_from_cart')

]
