# Generated by Django 3.1.4 on 2021-02-24 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0010_auto_20210222_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='themekanbancardfield',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
