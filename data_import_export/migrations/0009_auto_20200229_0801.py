# Generated by Django 2.2.2 on 2020-02-29 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_import_export', '0008_auto_20200221_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='import_files_data',
            name='file_data',
            field=models.TextField(),
        ),
    ]
