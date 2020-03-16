# Generated by Django 2.2.2 on 2020-03-13 07:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cms_manage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(blank=True, max_length=50)),
                ('title', models.CharField(blank=True, max_length=50)),
                ('help_description', models.TextField(blank=True)),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by_helpuser', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_by_helpuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'View move content manage',
            },
        ),
    ]
