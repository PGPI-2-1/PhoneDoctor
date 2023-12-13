# Generated by Django 4.2.7 on 2023-12-13 11:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_opinion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opinion',
            name='valoracion',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, message='La valoración no puede ser negativa'), django.core.validators.MaxValueValidator(5, message='La valoración no puede ser mayor que 5')]),
        ),
    ]
