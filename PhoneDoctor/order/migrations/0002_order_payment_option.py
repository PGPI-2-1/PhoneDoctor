# Generated by Django 4.2.7 on 2023-12-13 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('contra_reembolso', 'Contra reembolso'), ('tarjeta', 'Tarjeta')], default='contra_reembolso', max_length=20),
        ),
    ]
