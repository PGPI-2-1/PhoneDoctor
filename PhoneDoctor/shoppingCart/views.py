from django.shortcuts import render, redirect
from product.models import Product
from .models import CartItem


def add_to_cart(request, product_id):
    quantity = int(request.POST.get('quantity', 1))  # Obtener la cantidad del formulario, con 1 como valor predeterminado
    product = Product.objects.get(pk=product_id)

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    return redirect("/")


def getCartItems(request):
    shoppingCarts = CartItem.objects.filter(user_id=request.user.id)

    return render(request, 'core/base.html', context)




