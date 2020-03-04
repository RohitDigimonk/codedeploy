# Generated by Django 2.2.2 on 2020-03-04 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manage_backlogs', '0003_auto_20200229_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar_backlog_status',
            name='create_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_by_backlogstatus', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ar_backlog_status',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_by_backlogstatus', to=settings.AUTH_USER_MODEL),
        ),
    ]
