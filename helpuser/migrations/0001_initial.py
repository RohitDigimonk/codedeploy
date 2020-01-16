# Generated by Django 2.2.2 on 2020-01-09 14:26

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArHelpFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('help_topic_title', models.CharField(blank=True, max_length=50)),
                ('help_description', models.TextField(blank=True)),
                ('help_text', models.TextField(blank=True)),
                ('help_link_1', models.CharField(blank=True, max_length=50)),
                ('help_link_2', models.CharField(blank=True, max_length=50)),
                ('help_link_3', models.CharField(blank=True, max_length=50)),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='created_by_helpuser', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='updated_by_helpuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]