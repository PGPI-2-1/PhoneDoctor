from django.db import models
from custom_user.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural='Categories'

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural='Brands'

    def __str__(self):
        return self.name
    
class Product(models.Model):

    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description=models.TextField(blank=True,null=True)
    price=models.FloatField()
    image = models.ImageField(blank=True, null=True, upload_to='item_images')
    is_sold=models.BooleanField(default=False)

    def __str__(self):
        return self.name

