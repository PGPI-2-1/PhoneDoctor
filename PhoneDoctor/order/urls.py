from django.urls import path

from .views import checkout, seguimiento_pedido, my_orders, order_review
urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('<int:order_id>/', seguimiento_pedido, name='seguimiento_pedido'),
    path('my_orders', my_orders, name='my_orders'),
    path('review/<int:order_id>/', order_review, name='order_review')
]