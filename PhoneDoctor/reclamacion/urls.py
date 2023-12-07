from django.urls import path

from .views import nueva_reclamacion, reclamaciones, gestionar_reclamacion

urlpatterns = [
    path('new/', nueva_reclamacion, name ='nueva_reclamacion'),
    path('all/',reclamaciones, name='reclamaciones'),
    path('<int:reclamacion_id>/', gestionar_reclamacion, name='gestionar_reclamacion'),
]