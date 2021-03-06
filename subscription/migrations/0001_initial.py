# Generated by Django 2.2.2 on 2020-03-13 08:09

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_Done', models.BooleanField(blank=True, default=False)),
                ('Price', models.IntegerField(default=0, help_text="'0' Equal to 'Free'")),
                ('Active', models.BooleanField(blank=True, default=False)),
                ('Active_date', models.DateField(blank=True, null=True)),
                ('Role_access_and_security', models.BooleanField(blank=True, default=False)),
                ('Invite_user', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Team', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Product', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Backlog_per_Product', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Rating_cycle', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('User_story', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Time_duration_count', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Time_duration_type', models.CharField(default='Day', max_length=50)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Organization', models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='organization_by_membership_history', to='account.AR_organization')),
            ],
            options={
                'verbose_name_plural': 'AR Membership History',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(blank=True, max_length=50)),
                ('Price', models.IntegerField(default=0, help_text="'0' Equal to 'Free'")),
                ('Undefine_price', models.BooleanField(blank=True, default=False, help_text='Q1 2020')),
                ('Active', models.BooleanField(blank=True, default=False)),
                ('Role_access_and_security', models.BooleanField(blank=True, default=False)),
                ('Invite_user', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Team', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Product', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Backlog_per_Product', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Rating_cycle', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('User_story', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Time_duration_count', models.IntegerField(default=0, help_text="'0' Equal to 'Unlimited'")),
                ('Time_duration_type', models.CharField(default='Day', max_length=50)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('create_by', models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='create_by_subscription', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'AR Subscription',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_method', models.CharField(default='', max_length=80)),
                ('Payment_Done', models.BooleanField(blank=True, default=False)),
                ('Currency_type', models.CharField(default='$', max_length=50)),
                ('Transaction_id', models.CharField(default='', max_length=150)),
                ('Organization', models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='organization_by_payment', to='account.AR_organization')),
                ('Root_user', models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='root_user_by_membership_payment', to='account.Ar_user')),
                ('payment_port', models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='payment_id_by_payment', to='subscription.MembershipHistory')),
            ],
            options={
                'verbose_name_plural': 'AR Payment',
            },
        ),
        migrations.AddField(
            model_name='membershiphistory',
            name='Package_name',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='package_name_by_membership_history', to='subscription.Subscription'),
        ),
        migrations.AddField(
            model_name='membershiphistory',
            name='Root_user',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='root_user_by_membership_history', to='account.Ar_user'),
        ),
        migrations.AddField(
            model_name='membershiphistory',
            name='create_by',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete='models.SET_NULL', related_name='create_by_membership_history', to='account.Ar_user'),
        ),
    ]
