from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import loader
from .models import Product
from django.urls import reverse


# Create your views here.
from .forms import NewProductForm, EditProductForm, NewBrandForm,NewCategoryForm


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
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return render(request, 'product/404.html', {})

    return render(request, 'product/info.html', {
        'product': product
    })
