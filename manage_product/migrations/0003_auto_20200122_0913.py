# Generated by Django 2.2.2 on 2020-01-22 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_product', '0002_auto_20200114_0653'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ar_product',
            old_name='Procduct_description',
            new_name='Product_description',
        ),
        migrations.RenameField(
            model_name='ar_product',
            old_name='Procduct_name',
            new_name='Product_name',
        ),
    ]
