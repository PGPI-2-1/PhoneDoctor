from django.shortcuts import render
from product.models import Category, Product, Brand
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
    brands = Brand.objects.all()
    products = Product.objects.all()

    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    query = request.GET.get('q')

    if category and brand and query:
        products = Product.objects.filter(brand__name=brand, category__name=category, name__icontains=query)
    elif category and brand:
        products = Product.objects.filter(category__name=category, brand__name=brand)
    elif category and query:
        products = Product.objects.filter(category__name=category, name__icontains=query)
    elif brand and query:
        products = Product.objects.filter(brand__name=brand, name__icontains=query)
    elif category:
        products = Product.objects.filter(category__name=category)
    elif brand:
        products = Product.objects.filter(brand__name=brand)
    elif query: 
        products = Product.objects.filter(name__icontains=query)

    no_products = not products.exists()
    return render(request, 'core/index.html', {
        'categories': categories,
        'brands': brands,   
        'products': products,
        'category_filter': category,
        'brand_filter': brand,
        'cart_items':shoppingCarts,
        'precio_total':total,
        'mensaje':mensaje,
        'mensaje_cantidad':mensaje_cantidad,
        'no_products': no_products
    })

def calcular_total(items):
    precio_total=0
    for item in items:
        precio_por_cantidad = item.quantity * item.product.price
        precio_total = precio_total + precio_por_cantidad
    return precio_total

def about_us(request):   
    return render(request, 'core/about_us.html')