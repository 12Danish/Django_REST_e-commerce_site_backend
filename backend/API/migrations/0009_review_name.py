# Generated by Django 4.2.6 on 2023-11-27 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0008_remove_product_reviews'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='random', max_length=100),
        ),
    ]
