from django.db import models
from product.models import Product
from custom_user.models import User


class CartItem(models.Model):
    user = models.ForeignKey(User, related_name='cart_item', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    is_processed = models.BooleanField(default=False)
