from django.shortcuts import render, redirect
from django.views import View
from .forms import RegistrationForm

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
