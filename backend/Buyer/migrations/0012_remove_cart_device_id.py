# Generated by Django 4.2.6 on 2024-02-18 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0011_alter_cart_buyer_alter_cart_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='device_id',
        ),
    ]
