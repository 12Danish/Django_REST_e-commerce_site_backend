# Generated by Django 4.2.6 on 2024-03-05 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Buyer', '0013_rename_product_image_orderhistory_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderhistory',
            old_name='image',
            new_name='product_image',
        ),
    ]
