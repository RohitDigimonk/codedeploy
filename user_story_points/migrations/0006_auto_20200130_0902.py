# Generated by Django 2.2.2 on 2020-01-30 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_story_points', '0005_auto_20200116_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aruserstorypoints',
            name='Point_Key',
            field=models.CharField(default='Point_Key', max_length=50),
        ),
    ]