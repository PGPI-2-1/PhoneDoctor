from django.urls import path
from . import views
from .views import checkout, seguimiento_pedido, my_orders, order_review, marcar_enviado, marcar_completado

urlpatterns = [
    path('checkout', checkout, name='checkout'),
    path('<int:order_id>/', seguimiento_pedido, name='seguimiento_pedido'),
    path('order/', views.order_admin_view, name='order_admin_view'),
    path('my_orders', my_orders, name='my_orders'),
    path('review/<int:order_id>', order_review, name='order_review'),
    path('shopping-cart',views.shopping_cart,name='shopping_cart'),
    path('search_order', views.search_order, name='search_order'),
    path('marcar_enviado/<int:order_id>', marcar_enviado, name='marcar_enviado'),
    path('marcar_completado/<int:order_id>', marcar_completado, name='marcar_completado'),
    path('change_payment/<int:order_id>', views.change_payment, name='change_payment'),
]