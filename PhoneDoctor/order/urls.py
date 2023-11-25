from django.urls import path

from .views import checkout, seguimiento_pedido
urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('<int:order_id>/', seguimiento_pedido, name='seguimiento_pedido')
]