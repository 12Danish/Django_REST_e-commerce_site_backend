# Generated by Django 4.2.6 on 2024-01-31 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('UserManagement', '0001_initial'),
        ('Buyer', '0006_alter_orderhistory_product_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='buyer',
        ),
        migrations.AddField(
            model_name='cart',
            name='registered_buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cart',
            name='unregistered_buyer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UserManagement.anonymoususer'),
        ),
    ]
