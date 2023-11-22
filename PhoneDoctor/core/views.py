from django.shortcuts import render
from product.models import Category, Product
from shoppingCart.models import CartItem
# Create your views here.

def index(request):
    mensaje=""
    mensaje_cantidad=""
    products = Product.objects.all()
    categories = Category.objects.all()
    shoppingCarts = CartItem.objects.filter(user_id=request.user.id, is_processed=False)
    if 'carrito_vacio' in request.session:
        mensaje=request.session.pop('carrito_vacio',None)

    if 'cantidad_superada' in request.session:
        mensaje_cantidad=request.session.pop('cantidad_superada',None)
    total = calcular_total(shoppingCarts)
    return render(request, 'core/index.html', {
        'categories':categories,
        'products':products,
        'cart_items':shoppingCarts,
        'precio_total':total,
        'mensaje':mensaje,
        'mensaje_cantidad':mensaje_cantidad,
    })

def calcular_total(items):
    precio_total=0
    for item in items:
        precio_por_cantidad = item.quantity * item.product.price
        precio_total = precio_total + precio_por_cantidad
    return precio_total