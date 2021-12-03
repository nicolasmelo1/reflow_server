# Generated by Django 3.2.5 on 2021-12-02 03:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('integration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntegrationAuthenticationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'integration_authentication_type',
            },
        ),
        migrations.RemoveField(
            model_name='integrationauthentication',
            name='app_name',
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='access_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='extra_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='secret_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='integrationauthentication',
            name='authentication_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='integration.integrationauthenticationtype'),
        ),
    ]
