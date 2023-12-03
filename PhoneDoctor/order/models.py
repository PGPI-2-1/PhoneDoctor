from django.db import models
from custom_user.models import User
from shoppingCart.models import CartItem

class Review(models.Model):
    title = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.title

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PAGADO = 'pagado', 'Pagado'
        ENVIADO = 'enviado', 'Enviado'
        COMPLETADO = 'completado', 'Completado'

    #products = models.ManyToManyField(Product, related_name='order_products')
    items = models.ManyToManyField(CartItem, related_name='order_items')
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE, null=True)
    review = models.OneToOneField(Review, related_name='order_review', on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=None, null=True)
    shipping_cost = models.FloatField(default=10.0)
    precio_total = models.FloatField()

    @property
    def total_price_with_shipping(self):
        if self.precio_total > 100.0:
            return self.precio_total
        else:
            return self.precio_total + self.shipping_cost