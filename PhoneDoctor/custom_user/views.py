from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import RegistrationForm, MyAuthForm
from django.contrib.auth.views import LoginView
from order.models import Order, Review
from custom_user.models import User
from django.contrib.auth.decorators import user_passes_test


class RegistrationView(View):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Puedes agregar lógica adicional aquí, como enviar un correo de confirmación.
            return redirect('login')  # Redirige al usuario a la página de inicio de sesión
        return render(request, self.template_name, {'form': form})
    
class MyLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = MyAuthForm

    def form_invalid(self, form):
        # Llama al método padre para obtener el comportamiento predeterminado
        response = super().form_invalid(form)
        # Agrega mensajes de error al contexto de la plantilla
        error_messages = form.errors['__all__'] if '__all__' in form.errors else None
        self.request.session['error_messages'] = error_messages
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recupera mensajes de error del contexto de la sesión
        context['error_messages'] = self.request.session.pop('error_messages', None)
        return context

def order_admin_view(request):
    orders = Order.objects.all()

    return render(request, 'orders.html', {'orders': orders})    

def is_staff(user):
    return user.is_staff

@user_passes_test(is_staff, login_url='login')
def user_admin_view(request):
    users = User.objects.all()

    return render(request, "users.html",{'users': users})

def order_review(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    review = order.review

    return render(request, 'review.html', {'review': review})