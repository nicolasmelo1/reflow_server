# Generated by Django 3.1.4 on 2021-02-14 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0013_auto_20210213_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentcompanycharge',
            name='user',
        ),
    ]
