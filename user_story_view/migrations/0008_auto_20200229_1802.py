# Generated by Django 2.2.2 on 2020-02-29 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_story_view', '0007_auto_20200224_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar_us_status',
            name='create_by',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='create_by_us_status', to='account.Ar_user'),
        ),
        migrations.AlterField(
            model_name='ar_us_status',
            name='update_by',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='update_by_us_status', to='account.Ar_user'),
        ),
    ]
