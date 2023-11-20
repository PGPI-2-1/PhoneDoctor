from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from shoppingCart.models import CartItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def checkout(request):
    if not request.user.is_authenticated:      
        cart_items = CartItem.objects.filter(user=None)
    else:
        cart_items = CartItem.objects.filter(user=request.user)

    if len(cart_items) == 0:
        request.session['carrito_vacio'] = "El carrito no puede estar vacío"
        return redirect("/")

    precio_total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if request.method == 'POST':

        address = request.POST.get('address')

        if request.user.is_authenticated:
            order = Order.objects.create(user=request.user, address=address, is_paid=True)
            order.products.set([item.product for item in cart_items])
            order.save()
            enviar_correo(request,address,precio_total,cart_items,request.user.email)
        else:
            email = request.POST.get('email')
            order = Order.objects.create(user=None, address=address, email=email, is_paid=True)
            order.products.set([item.product for item in cart_items])
            order.save()
            enviar_correo(request,address,precio_total,cart_items,email)


        cart_items.delete()

        return redirect('/')  

    context = {
        'cart_items': cart_items,
        'precio_total': precio_total,
    }

    return render(request, 'checkout.html', context)

def enviar_correo(request,address,precio_total,cart_items,email):
    subject = 'Confirmación de Pedido'
    message = render_to_string('email/order_confirmation.html', {'email':email,'address': address, 'precio_total':precio_total, 'cart_items':cart_items})
    plain_message = strip_tags(message)
    from_email = 'phonedoctorPGPI@outlook.es'  # Cambia esto con tu dirección de correo electrónico
    to_email = [email]  # Utiliza el correo electrónico del usuario que realizó la orden

    send_mail(subject, plain_message, from_email, to_email, html_message=message)
