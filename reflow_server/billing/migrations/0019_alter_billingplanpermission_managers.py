# Generated by Django 3.2.5 on 2021-12-15 14:01

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0018_alter_billingplanpermission_default_quantity'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='billingplanpermission',
            managers=[
                ('billing_', django.db.models.manager.Manager()),
            ],
        ),
    ]
