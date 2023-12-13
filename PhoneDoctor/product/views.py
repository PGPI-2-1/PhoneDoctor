from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import loader
from .models import Product
from django.urls import reverse
from shoppingCart.models import CartItem
from core.views import calcular_total
from order.models import Order


from .forms import NewProductForm, EditProductForm, NewBrandForm,NewCategoryForm, NewOpinionForm


@login_required
def new_category(request):
    form = NewCategoryForm()
    if not request.user.is_staff:
        template = loader.get_template('product/403.html')
        return HttpResponseForbidden(template.render({}, request))

    if request.method == 'POST':
        form = NewCategoryForm(request.POST, request.FILES)

        if form.is_valid():
            item=form.save(commit=False)
            item.save()

            return redirect('/')
        else:
            form = NewCategoryForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Nueva Categoria',
    })
    
@login_required
def new_brand(request):
    form = NewBrandForm()
    if not request.user.is_staff:
        template = loader.get_template('product/403.html')
        return HttpResponseForbidden(template.render({}, request))

    if request.method == 'POST':
        form = NewBrandForm(request.POST, request.FILES)

        if form.is_valid():
            item=form.save(commit=False)
            item.save()

            return redirect('/')
        else:
            form = NewBrandForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Nueva Marca',
    })
    
@login_required
def new(request):

    if not request.user.is_staff:
        template = loader.get_template('product/403.html')
        return HttpResponseForbidden(template.render({}, request))

    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)

        if form.is_valid():
            item=form.save(commit=False)
            item.save()

            return redirect('/')
    else:
        form = NewProductForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Nuevo Producto',
    })

@login_required
def delete(request, pk):
    if not request.user.is_staff:
        template = loader.get_template('product/403.html')
        return HttpResponseForbidden(template.render({}, request))
    else:
        product=get_object_or_404(Product, pk=pk)
        product.delete()

        return redirect('/')

@login_required
def edit(request, pk):
    product=get_object_or_404(Product, pk=pk)

    if not request.user.is_staff:
        template = loader.get_template('product/403.html')
        return HttpResponseForbidden(template.render({}, request))

    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            return redirect('/')
    else:
        form = EditProductForm(instance=product)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Modificar Producto',
    })

def product_info(request, pk):
    try:
        mensaje=""
        mensaje_cantidad=""
        product = Product.objects.get(pk=pk)
        shoppingCarts = CartItem.objects.filter(user_id=request.user.id, is_processed=False)
        if 'carrito_vacio' in request.session:
            mensaje=request.session.pop('carrito_vacio',None)

        if 'cantidad_superada' in request.session:
            mensaje_cantidad=request.session.pop('cantidad_superada',None)
        total = calcular_total(shoppingCarts)
    except Product.DoesNotExist:
        return render(request, 'product/404.html', {})

    return render(request, 'product/info.html', {
        'product': product,
        'cart_items':shoppingCarts,
        'precio_total':total,
        'mensaje':mensaje,
        'mensaje_cantidad':mensaje_cantidad,
    })

def nueva_opinion(request, product_id):
    if not request.user.is_authenticated:
        template = loader.get_template('opinion/403.html')
        return HttpResponseForbidden(template.render({}, request))
    
    product=get_object_or_404(Product, id=product_id)
    user = request.user
    orders_by_user = Order.objects.filter(user=user)
    products_by_user=[]
    for order in orders_by_user:
        for item in order.items.all():
            products_by_user.append(item.product.id)

    if not product_id in products_by_user:
        template = loader.get_template('opinion/403.html')
        return HttpResponseForbidden(template.render({}, request))
    else:
        if request.method == 'POST':
            form = NewOpinionForm(request.POST, request.FILES)

            if form.is_valid():
                print("holaquetal")
                opinion=form.save(commit=False)
                opinion.product=product
                opinion.user=user
                opinion.save()

                return redirect('/')
        else:
            form = NewOpinionForm()

        return render(request, 'opinion/form.html', {
            'form': form,
            'title': 'Nueva Opinion',
        })