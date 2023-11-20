from django.shortcuts import render
from product.models import Category, Product
from shoppingCart.models import CartItem
# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    shoppingCarts = CartItem.objects.filter(user_id=request.user.id)
    return render(request, 'core/index.html', {
        'categories':categories,
        'products':products,
        'cart_items':shoppingCarts,
    })