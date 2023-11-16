from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.template import loader


# Create your views here.
from .forms import NewProductForm

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
            #return redirect('product:detail', pk=product.id)
    else:
        form = NewProductForm()

    return render(request, 'product/form.html', {
        'form': form,
        'title': 'Nuevo Producto',
    })
