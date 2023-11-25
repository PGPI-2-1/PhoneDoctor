from django.db import models
from product.models import Product
from custom_user.models import User
from shoppingCart.models import CartItem

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PAGADO = 'pagado', 'Pagado'
        ENVIADO = 'enviado', 'Enviado'
        COMPLETADO = 'completado', 'Completado'

    #products = models.ManyToManyField(Product, related_name='order_products')
    items = models.ManyToManyField(CartItem, related_name='order_items')
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=False, blank=False)
    email =models.EmailField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=None, null=True)
    precio_total=models.FloatField()