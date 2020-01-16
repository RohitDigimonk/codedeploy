# Generated by Django 2.2.2 on 2020-01-09 07:09

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('manage_backlogs', '0001_initial'),
        ('user_story_view', '0001_initial'),
        ('account', '0001_initial'),
        ('manage_product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArIterations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IterationName', models.CharField(blank=True, max_length=50)),
                ('owner', models.CharField(blank=True, max_length=50)),
                ('IterationId', models.TextField(max_length=50)),
                ('StartDate', models.DateTimeField()),
                ('EndDate', models.DateTimeField()),
                ('Description', models.TextField()),
                ('IterationScore', models.IntegerField(blank=True)),
                ('IterationSize', models.IntegerField(blank=True)),
                ('create_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('Backlog', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='backlogArIterations', to='manage_backlogs.AR_BACKLOG')),
                ('ORG_ID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teamArIterations', to='account.AR_organization')),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='productArIterations', to='manage_product.AR_product')),
                ('Team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teamArIterations', to='manage_product.AR_team')),
                ('UserStory', models.ManyToManyField(blank=True, default='', related_name='userstoryArIterations', to='user_story_view.AR_USER_STORY')),
                ('create_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='create_by_iterations', to='account.Ar_user')),
                ('update_by', models.ForeignKey(on_delete='models.SET_NULL', related_name='update_by_iterations', to='account.Ar_user')),
            ],
        ),
    ]