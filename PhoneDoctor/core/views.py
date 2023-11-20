from django.shortcuts import render
from product.models import Category, Product
from shoppingCart.models import CartItem
# Create your views here.

def index(request):
    mensaje=""
    products = Product.objects.all()
    categories = Category.objects.all()
    shoppingCarts = CartItem.objects.filter(user_id=request.user.id)
    if 'carrito_vacio' in request.session:
        mensaje=request.session.pop('carrito_vacio',None)
    total = calcular_total(shoppingCarts)
    return render(request, 'core/index.html', {
        'categories':categories,
        'products':products,
        'cart_items':shoppingCarts,
        'precio_total':total,
        'mensaje':mensaje,
    })

def calcular_total(items):
    precio_total=0
    for item in items:
        precio_por_cantidad = item.quantity * item.product.price
        precio_total = precio_total + precio_por_cantidad
    return precio_total