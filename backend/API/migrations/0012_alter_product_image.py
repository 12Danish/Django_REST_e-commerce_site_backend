# Generated by Django 4.2.6 on 2024-03-04 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0011_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]