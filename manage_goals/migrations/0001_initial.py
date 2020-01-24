# Generated by Django 2.2.9 on 2020-01-18 08:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0002_auto_20200114_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArManageGoals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Goal_id', models.CharField(blank=True, max_length=50, null=True)),
                ('Goal_title', models.CharField(blank=True, max_length=50, null=True)),
                ('Gole_description', models.TextField()),
                ('Use_in', models.TextField()),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('ORG_ID', models.ForeignKey(default='', null=True, on_delete='models.SET_NULL', to='account.AR_organization')),
                ('created_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='create_by_ManageGoals', to='account.Ar_user')),
                ('updated_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='update_by_ManageGoals', to='account.Ar_user')),
            ],
        ),
    ]
