# Generated by Django 2.2.2 on 2020-01-15 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_backlogs', '0002_auto_20200114_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar_backlog',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
