# Generated by Django 3.2.5 on 2021-10-25 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0013_apiaccesstoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiaccesstoken',
            name='access_token',
            field=models.CharField(blank=True, db_index=True, max_length=500, null=True),
        ),
    ]
