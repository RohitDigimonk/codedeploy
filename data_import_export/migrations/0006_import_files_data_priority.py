# Generated by Django 2.2.2 on 2020-02-17 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_import_export', '0005_import_files_data_upload_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='import_files_data',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
