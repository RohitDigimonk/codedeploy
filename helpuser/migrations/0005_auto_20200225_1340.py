# Generated by Django 2.2.2 on 2020-02-25 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpuser', '0004_auto_20200225_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cms_manage',
            name='keyword',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
