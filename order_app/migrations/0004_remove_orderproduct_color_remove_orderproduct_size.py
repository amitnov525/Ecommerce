# Generated by Django 4.1.1 on 2022-10-07 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order_app', '0003_alter_order_order_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='color',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='size',
        ),
    ]
