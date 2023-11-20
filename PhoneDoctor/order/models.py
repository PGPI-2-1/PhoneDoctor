from django.db import models
from product.models import Product
from custom_user.models import User

class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='order_products')
    user = models.ForeignKey(User, related_name='order_user', on_delete=models.CASCADE, null=True)
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=False, blank=False)
    email =models.EmailField(max_length=100, null=True)