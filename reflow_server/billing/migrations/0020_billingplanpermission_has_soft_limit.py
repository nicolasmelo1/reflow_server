# Generated by Django 3.2.5 on 2021-12-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0019_alter_billingplanpermission_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingplanpermission',
            name='has_soft_limit',
            field=models.BooleanField(default=False),
        ),
    ]
