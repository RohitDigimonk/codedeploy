# Generated by Django 2.2.2 on 2020-01-13 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_features', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar_feature',
            name='CE_ID',
            field=models.ForeignKey(default='', null=True, on_delete='models.SET_NULL', to='manage_epic_capability.AR_EPIC_CAPABILITY'),
        ),
    ]
