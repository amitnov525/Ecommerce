# Generated by Django 4.1.1 on 2022-09-23 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_alter_variation_variation_category'),
        ('cart_app', '0002_rename_cart_id_cart_cartid'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variation',
            field=models.ManyToManyField(blank=True, to='store_app.variation'),
        ),
    ]
