from django.urls import path

from .views import add_to_cart, getCartItems
urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('getCartItems/', getCartItems, name='get_cart_items'),
]