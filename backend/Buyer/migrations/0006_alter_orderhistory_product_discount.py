# Generated by Django 4.2.6 on 2024-01-16 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0005_alter_orderhistory_product_discount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='product_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]