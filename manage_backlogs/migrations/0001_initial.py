# Generated by Django 2.2.2 on 2020-02-04 05:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manage_product', '0001_initial'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AR_BACKLOG_STATUS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bl_status_key', models.CharField(blank=True, max_length=50)),
                ('bl_status_desc', models.TextField(blank=True)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_by_backlogstatus', to='account.Ar_user')),
                ('update_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_by_backlogstatus', to='account.Ar_user')),
            ],
        ),
        migrations.CreateModel(
            name='AR_BACKLOG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('backlog_score', models.IntegerField()),
                ('Backlog_size', models.IntegerField()),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('BL_STATUS', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_backlogs.AR_BACKLOG_STATUS')),
                ('ORG_ID', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.AR_organization')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='create_by_backlog', to='account.Ar_user')),
                ('owner', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.Ar_user')),
                ('product_parent', models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backlog_by_product', to='manage_product.AR_product')),
                ('team_list', models.ManyToManyField(blank=True, related_name='backlog_team', to='manage_product.AR_team')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_by_backlog', to='account.Ar_user')),
            ],
        ),
    ]
