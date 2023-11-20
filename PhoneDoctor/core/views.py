from django.shortcuts import render
from product.models import Category, Product, Brand

def index(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()

    category = request.GET.get('category', None)
    brand = request.GET.get('brand', None)
    query = request.GET.get('q')

    if category and brand:
        products = Product.objects.filter(brand__name=brand, category__name=category)
    elif category:
        products = Product.objects.filter(category__name=category)
    elif brand:
        products = Product.objects.filter(brand__name=brand)
    elif query: 
        products = Product.objects.filter(name__icontains=query)
       
   


    return render(request, 'core/index.html', {
        'categories': categories,
        'brands': brands,
        'products': products,
        'category_filter': category,
        'brand_filter': brand,
    })
