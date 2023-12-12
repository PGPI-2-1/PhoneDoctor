from django.http import HttpResponse
from django.shortcuts import render, redirect
from product.models import Product
from .models import CartItem



def add_to_cart(request, product_id):

    cantidad_ingresada_str = request.GET.get('cantidad', 0)
    cantidad_ingresada = int(cantidad_ingresada_str)
    product = Product.objects.get(pk=product_id)

    if request.user.is_authenticated:
        cart_item_tuple= CartItem.objects.get_or_create(user=request.user, product=product, is_processed=False)
        cart_item = cart_item_tuple[0]
    else:
        cart_item_tuple= CartItem.objects.get_or_create(user=None, product=product, is_processed=False)
        cart_item = cart_item_tuple[0]

    if cantidad_ingresada == 0:
        cart_item.delete()
    elif product.quantity >= cantidad_ingresada:
        cart_item.quantity = cantidad_ingresada
        cart_item.save()
    else:
        cart_item.delete()
        request.session['cantidad_superada'] = "No quedan tantas unidades de este producto"
    
    return redirect(request.META.get('HTTP_REFERER', '/'))






