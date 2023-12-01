from django.urls import path
from . import views
from .views import checkout, seguimiento_pedido

urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('<int:order_id>/', seguimiento_pedido, name='seguimiento_pedido'),
    path('order/', views.order_admin_view, name='order_admin_view'),
    path('shopping-cart',views.shopping_cart,name='shopping_cart')
]