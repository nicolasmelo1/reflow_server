# Generated by Django 3.0.6 on 2020-08-04 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0005_auto_20200804_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companycharge',
            name='charge_date',
        ),
        migrations.RemoveField(
            model_name='companycharge',
            name='due_date',
        ),
    ]
