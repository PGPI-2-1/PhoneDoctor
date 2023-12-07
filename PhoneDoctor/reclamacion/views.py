from django.shortcuts import render, redirect
from .forms import NewReclamacionForm
from django.template.loader import render_to_string
from .models import Reclamacion
from django.utils.html import strip_tags
from django.core.mail import send_mail

# Create your views here.

def nueva_reclamacion(request):
    form = NewReclamacionForm()
    if not request.user.is_authenticated:
        return render(request, 'reclamacion/403.html')

    if request.method == 'POST':
        form = NewReclamacionForm(request.POST, request.FILES)

        if form.is_valid():
            item=form.save(commit=False)
            item.user=request.user
            item.save()

            return redirect('/')
        else:
            form = NewReclamacionForm()

    return render(request, 'reclamacion/form.html', {
        'form': form,
        'title': 'Nueva Reclamacion',
    })

def reclamaciones(request):
    if not request.user.is_staff:
        return render(request, 'reclamacion/403.html')
    
    reclamaciones = Reclamacion.objects.all()

    return render(request, 'reclamacion/reclamaciones.html', {'reclamaciones': reclamaciones})

def gestionar_reclamacion(request, reclamacion_id):
    reclamacion=Reclamacion.objects.get(id=reclamacion_id)
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        email = reclamacion.user.email
        enviar_correo(request,reclamacion.fecha, mensaje, email, reclamacion.descripcion )
        reclamacion.status=Reclamacion.StatusReclamacion.SOLUCIONADO
        reclamacion.save()
        return redirect('/')
    
    return render(request, 'reclamacion/gestionar_reclamacion.html', {'reclamacion': reclamacion})


def enviar_correo(request, fecha, mensaje, email, descripcion):
    subject = 'Gestión de Reclamación'
    message = render_to_string('email/gestionar_reclamacion.html', {'email':email,'fecha': fecha, 'mensaje':mensaje, 'descripcion':descripcion})
    plain_message = strip_tags(message)
    from_email = 'phonedoctorPGPI@outlook.es' 
    to_email = [email] 

    send_mail(subject, plain_message, from_email, to_email, html_message=message)

    
