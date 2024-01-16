# Generated by Django 4.2.6 on 2024-01-15 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0004_remove_orderhistory_product_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='product_discount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='product_price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='quantity',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
