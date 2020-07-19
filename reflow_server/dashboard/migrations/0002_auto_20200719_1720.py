# Generated by Django 3.0.6 on 2020-07-19 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aggregationtype',
            options={'ordering': ('order',)},
        ),
        migrations.AlterModelOptions(
            name='charttype',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='aggregationtype',
            name='order',
            field=models.BigIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='charttype',
            name='order',
            field=models.BigIntegerField(default=1),
        ),
    ]
