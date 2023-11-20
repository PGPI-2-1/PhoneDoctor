from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import loader
from .models import Product


# Create your views here.
from .forms import NewProductForm, EditProductForm

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
            #return redirect('product:detail', pk=product.id)
    else:
        form = EditProductForm(instance=product)

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Modificar Producto',
    })
