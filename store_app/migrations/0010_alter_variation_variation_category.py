# Generated by Django 4.1.1 on 2022-10-14 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0009_alter_reviewrating_ip_alter_reviewrating_review_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size')], max_length=100),
        ),
    ]
