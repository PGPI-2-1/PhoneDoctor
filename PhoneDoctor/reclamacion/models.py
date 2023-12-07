from django.db import models
from custom_user.models import User

# Create your models here.
class Reclamacion(models.Model):
    class StatusReclamacion(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        SOLUCIONADO = 'solucionado', 'Solucionado'

    user = models.ForeignKey(User, related_name='reclamacion_user', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=StatusReclamacion.choices, default=StatusReclamacion.PENDIENTE)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=255, blank=False, null=False)