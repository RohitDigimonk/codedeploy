# Generated by Django 2.2.2 on 2020-03-13 07:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AR_team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team_name', models.CharField(max_length=100)),
                ('Team_description', models.TextField()),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('ORG_id', models.ForeignKey(default='', null=True, on_delete='models.CASCADE', to='account.AR_organization')),
                ('Team_member_list', models.ManyToManyField(blank=True, related_name='user_data', to='account.Ar_user')),
                ('create_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='create_by_team', to='account.Ar_user')),
                ('update_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='update_by_team', to='account.Ar_user')),
            ],
            options={
                'verbose_name_plural': 'Ar team',
                'unique_together': {('Team_name', 'ORG_id')},
            },
        ),
        migrations.CreateModel(
            name='AR_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_name', models.CharField(max_length=50)),
                ('Product_description', models.TextField()),
                ('Business_unit', models.CharField(max_length=100)),
                ('Product_size', models.IntegerField(default=0)),
                ('Product_score', models.IntegerField(default=0)),
                ('US_quality_threshold', models.IntegerField(default=0)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('ORG_ID', models.ForeignKey(default='', null=True, on_delete='models.SET_NULL', to='account.AR_organization')),
                ('Team_parent', models.ManyToManyField(blank=True, related_name='user_favourite', to='manage_product.AR_team')),
                ('create_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='create_by_product', to='account.Ar_user')),
                ('update_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='update_by_product', to='account.Ar_user')),
            ],
            options={
                'verbose_name_plural': 'Ar product',
            },
        ),
    ]
