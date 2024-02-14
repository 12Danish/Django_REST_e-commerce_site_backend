# Generated by Django 4.2.6 on 2024-02-13 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_alter_product_price'),
        ('Buyer', '0009_alter_cart_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='device_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='API.product'),
        ),
    ]
