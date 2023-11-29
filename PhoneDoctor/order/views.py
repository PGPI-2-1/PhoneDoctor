from django.shortcuts import render, redirect
from .models import Order
from shoppingCart.models import CartItem
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def checkout(request):
    if not request.user.is_authenticated:      
        cart_items = CartItem.objects.filter(user=None, is_processed = False)
    else:
        cart_items = CartItem.objects.filter(user=request.user, is_processed=False)

    if len(cart_items) == 0:
        request.session['carrito_vacio'] = "El carrito no puede estar vacío"
        return redirect("/")

    precio_total = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)

    if request.method == 'POST':

        address = request.POST.get('address')

        if request.user.is_authenticated:
            email = request.user.email
            order = Order.objects.create(user=request.user, address=address, email=email,status=Order.StatusChoices.PAGADO, precio_total=precio_total)
            order.items.set([item for item in cart_items])
            for item in cart_items:
                producto=item.product
                cantidad_antigua=producto.quantity
                producto.quantity=cantidad_antigua-item.quantity
                producto.save()
            order.save()
            #enviar_correo(request,address,precio_total,cart_items,request.user.email)
        else:
            email = request.POST.get('email')
            order = Order.objects.create(user=None, address=address, email=email, status=Order.StatusChoices.PAGADO, precio_total=precio_total)
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
    }

    return render(request, 'checkout.html', context)

def enviar_correo(request,address,precio_total,cart_items,email):
    subject = 'Confirmación de Pedido'
    message = render_to_string('email/order_confirmation.html', {'email':email,'address': address, 'precio_total':precio_total, 'cart_items':cart_items})
    plain_message = strip_tags(message)
    from_email = 'phonedoctorPGPI@outlook.es' 
    to_email = [email] 

    send_mail(subject, plain_message, from_email, to_email, html_message=message)

def seguimiento_pedido(request,order_id):
    order = Order.objects.get(id=order_id)

    return render(request,'seguimiento_pedido.html',{'order':order})

def order_admin_view(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'orders.html', context)