from django.db import models
from custom_user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    price=models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    quantity=models.IntegerField(default=0)
    is_sold=models.BooleanField(default=False)

    def __str__(self):
        return self.name

