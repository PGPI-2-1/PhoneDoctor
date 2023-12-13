from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from shoppingCart.models import CartItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import NewReviewForm
import secrets 
from .models import Review
from django.contrib.auth.decorators import user_passes_test
import stripe
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden



stripe.api_key = "sk_test_51OHPZ9JkuoHLkF3tWqXW9fp8DYhNOJS52uFwcaWmwiIxX5uL7DjU8nWx4mqyvVZsqLBPFFwXFxVdLSKT71O5c1JV00DuU1Cp7O"

def generate_unique_random_string(length=10):
    while True: 
        random_string = secrets.token_urlsafe(length)[:length]
        if not Order.objects.filter(id_tracking=random_string).exists():
            break
    return random_string

def checkout(request):
    if not request.user.is_authenticated:      
        cart_items = CartItem.objects.filter(user=None, is_processed = False)
    else:
        cart_items = CartItem.objects.filter(user=request.user, is_processed=False)

    if len(cart_items) == 0:
        request.session['carrito_vacio'] = "El carrito no puede estar vacío"
        return redirect("/")

    precio_total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if precio_total > 100.0:
        shipping_cost = 0.0
    else:
        shipping_cost = 10.0

    precio_total_con_envio = precio_total + shipping_cost

    if request.method == 'POST':
        payment_option = request.POST.get('payment_option')

        if payment_option == 'tarjeta':
            delivery_option = request.POST.get('delivery_option')
            token = request.POST.get('stripeToken')
            try:
                charge = stripe.Charge.create(
                    amount=int(precio_total*100),
                    currency='eur',
                    description='Compra en PhoneDoctor',
                    source=token,
                )

                address = request.POST.get('address')

                if request.user.is_authenticated:
                    email = request.user.email

                    #generar token unico para cada pedido: 
                    tracking = generate_unique_random_string()

                    order = Order.objects.create(user=request.user, address=address, email=email,status=Order.StatusChoices.PROCESADO, precio_total=precio_total, shipping_cost=shipping_cost, id_tracking = tracking, delivery_option=delivery_option,payment_option=Order.PaymentOptions.TARJETA)

                    order.items.set([item for item in cart_items])
                    for item in cart_items:
                        producto=item.product
                        cantidad_antigua=producto.quantity
                        producto.quantity=cantidad_antigua-item.quantity
                        producto.save()
                    order.save()
                    #enviar_correo(request,address,precio_total,cart_items,request.user.email)
                else:
                    #generar token unico para cada pedido: 
                    tracking = generate_unique_random_string()
                    email = request.POST.get('email')

                    order = Order.objects.create(user=None, address=address, email=email, status=Order.StatusChoices.PROCESADO, precio_total=precio_total, shipping_cost=shipping_cost, id_tracking = tracking, delivery_option=delivery_option, payment_option=Order.PaymentOptions.TARJETA)

                    order.items.set([item for item in cart_items])
                    for item in cart_items:
                        producto=item.product
                        cantidad_antigua=producto.quantity
                        producto.quantity=cantidad_antigua-item.quantity
                        producto.save()
                    order.save()
                    #enviar_correo(request,address,precio_total,cart_items,email)

                for cart_item in cart_items:
                    cart_item.is_processed=True
                    cart_item.save()

                return redirect('/order/'+str(order.id)+'/')  


            except stripe.error.CardError as e:
                # Si hay un error con la tarjeta, maneja la excepción y muestra un mensaje al usuario
                error_message = e.error.message
                context = {
                    'cart_items': cart_items,
                    'precio_total': precio_total_con_envio,
                    'shipping_cost': shipping_cost,
                    'error_message': error_message,
                }
                return render(request, 'checkout.html', context)
        elif payment_option == 'contra_reembolso':
            address = request.POST.get('address')
            delivery_option = request.POST.get('delivery_option')
            if request.user.is_authenticated:
                email = request.user.email
                    #generar token unico para cada pedido: 
                tracking = generate_unique_random_string()

                order = Order.objects.create(user=request.user, address=address, email=email,status=Order.StatusChoices.PROCESADO, precio_total=precio_total, shipping_cost=shipping_cost, id_tracking = tracking, delivery_option=delivery_option, payment_option=Order.PaymentOptions.CONTRA_REEMBOLSO)

                order.items.set([item for item in cart_items])
                for item in cart_items:
                    producto=item.product
                    cantidad_antigua=producto.quantity
                    producto.quantity=cantidad_antigua-item.quantity
                    producto.save()
                order.save()
                #enviar_correo(request,address,precio_total,cart_items,request.user.email)
            else:
                #generar token unico para cada pedido: 
                tracking = generate_unique_random_string()
                email = request.POST.get('email')

                order = Order.objects.create(user=None, address=address, email=email, status=Order.StatusChoices.PROCESADO, precio_total=precio_total, shipping_cost=shipping_cost, id_tracking = tracking, delivery_option=delivery_option, payment_option=Order.PaymentOptions.CONTRA_REEMBOLSO)

                order.items.set([item for item in cart_items])
                for item in cart_items:
                    producto=item.product
                    cantidad_antigua=producto.quantity
                    producto.quantity=cantidad_antigua-item.quantity
                    producto.save()
                order.save()
                #enviar_correo(request,address,precio_total,cart_items,email)

            for cart_item in cart_items:
                cart_item.is_processed=True
                cart_item.save()

            return redirect('/order/'+str(order.id)+'/')

    context = {
    'cart_items': cart_items,
    'precio_total': precio_total,
    'precio_total_con_envio': precio_total_con_envio,
    'shipping_cost': shipping_cost,
    }


    return render(request, 'checkout.html', context)

def enviar_correo(request, address, precio_total, cart_items, email):
    subject = 'Confirmación de Pedido'
    message = render_to_string('email/order_confirmation.html', {'email':email,'address': address, 'precio_total':precio_total, 'cart_items':cart_items})
    plain_message = strip_tags(message)
    from_email = 'phonedoctorPGPI@outlook.es' 
    to_email = [email] 

    send_mail(subject, plain_message, from_email, to_email, html_message=message)

def seguimiento_pedido(request,order_id):
    order = Order.objects.get(id=order_id)

    return render(request,'seguimiento_pedido.html', {'order':order})

def my_orders(request):
    orders = Order.objects.filter(user=request.user.id)

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_delivery_option = request.POST.get('new_delivery_option')
        payment_option = request.POST.get('payment_option')

        order = Order.objects.get(id=order_id)

        if order.status == Order.StatusChoices.PROCESADO:
            new_address = request.POST.get('new_address')
            if new_address:
                order.address = new_address
            order.delivery_option = new_delivery_option

            if payment_option == 'tarjeta':
                token = request.POST.get('stripeToken')
                try:
                    charge = stripe.Charge.create(
                        amount=int(order.precio_total * 100),
                        currency='eur',
                        description='Pago de pedido',
                        source=token,
                    )

                    order.status = Order.StatusChoices.PAGO_COMPLETADO
                    order.payment_option = 'tarjeta'
                    order.save()

                    # Realizar las acciones necesarias después de un pago exitoso, si es necesario

                except stripe.error.CardError as e:
                    # Manejar errores de tarjeta, puedes mostrar un mensaje al usuario o realizar otras acciones
                    error_message = e.error.message
                    context = {
                        'orders': orders,
                        'error_message': error_message,
                    }
                    return render(request, 'my_orders.html', context)

            # Resto de la lógica para cambiar la dirección y la opción de entrega

            order.save()

    return render(request, 'my_orders.html' , {'orders': orders})

def change_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Comprobar si el método de pago es 'contra reembolso'
    if order.payment_option != 'contra_reembolso':
        return HttpResponseForbidden("No puedes cambiar el método de pago para este pedido.")

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(order.precio_total * 100),
                currency='eur',
                description='Pago de pedido',
                source=token,
            )

            order.payment_option = 'tarjeta'
            order.save()

            # Realizar las acciones necesarias después de un pago exitoso, si es necesario

        except stripe.error.CardError as e:
            # Manejar errores de tarjeta, puedes mostrar un mensaje al usuario o realizar otras acciones
            error_message = e.error.message
            context = {
                'order': order,
                'error_message': error_message,
            }
            return render(request, 'change_payment.html', context)

        # Redirigir a la vista de los pedidos después de realizar el pago
        return redirect('my_orders')

    # Si el método de la solicitud no es 'POST', renderizar la plantilla 'change_payment.html'
    return render(request, 'change_payment.html', {'order': order})


def order_review(request, order_id):
    order = Order.objects.get(pk=order_id)

    if request.user != order.user:
        return render(request, '403.html')

    if request.method == 'POST':
        form = NewReviewForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.is_accepted = Review.AcceptionStatus.PENDING
            item.save()
            order.review = item
            order.save()
            return redirect('/order/my_orders')
    else:
        form = NewReviewForm()

    return render(request, 'form.html', {
        'form': form,
        'title': 'Nueva Reclamación',
        'order': order,
    })


def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='login')
def order_admin_view(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'orders.html', context)


def shopping_cart(request):
    if not request.user.is_authenticated:      
        cart_items = CartItem.objects.filter(user=None, is_processed = False)
    else:
        cart_items = CartItem.objects.filter(user=request.user, is_processed=False)

    if len(cart_items) == 0:
        precio_total = 0
    else:
        precio_total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if precio_total > 100.0:
        shipping_cost = 0.0
    else:
        shipping_cost = 10.0

    precio_total_con_envio = precio_total + shipping_cost

    context = {
    'cart_items': cart_items,
    'precio_total': precio_total,
    'precio_total_con_envio': precio_total_con_envio,
    'shipping_cost': shipping_cost,
    }

    return render(request, 'shopping_cart.html', context)

def search_order(request): 
    query = request.GET.get('q', '').strip() 

    if(Order.objects.filter(id_tracking = query)): 
        order = get_object_or_404(Order, id_tracking=query) 
        return render(request, 'seguimiento_pedido.html', {'order': order}) 
    else:
       return render(request, '404.html')
    
def marcar_enviado(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = Order.StatusChoices.ENVIADO
    order.save()

    return render(request,'seguimiento_pedido.html', {'order':order})

def marcar_completado(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = Order.StatusChoices.COMPLETADO
    order.save()

    return render(request,'seguimiento_pedido.html', {'order':order})