# Generated by Django 2.2.2 on 2020-01-27 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20200127_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arhelpcontect',
            name='Page_slug',
            field=models.CharField(blank=True, help_text='Copy URL after the http://203.190.153.20/ and past', max_length=250, null=True),
        ),
    ]