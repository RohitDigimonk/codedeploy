# Generated by Django 2.2.2 on 2020-01-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200116_1001'),
        ('manage_role', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrole',
            name='ORG_ID',
            field=models.ForeignKey(default='', null=True, on_delete='models.SET_NULL', to='account.AR_organization'),
        ),
    ]
