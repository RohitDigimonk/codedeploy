# Generated by Django 2.2.2 on 2020-01-25 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_backlogs', '0004_auto_20200115_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar_backlog',
            name='children_us_list',
            field=models.TextField(blank=True),
        ),
    ]