from django.shortcuts import render
from product.models import Category, Product
# Create your views here.

def index(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories':categories,
        'products':products,
    })