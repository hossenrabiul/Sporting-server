# Generated by Django 5.1.4 on 2025-02-16 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('posts', '0002_remove_products_brand_alter_products_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Brand',
        ),
    ]
