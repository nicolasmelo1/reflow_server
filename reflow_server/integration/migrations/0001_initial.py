# Generated by Django 3.2.5 on 2021-09-09 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IntegrationAuthentication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'integration_authentication',
            },
        ),
    ]
