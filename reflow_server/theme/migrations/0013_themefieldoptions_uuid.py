# Generated by Django 3.1.4 on 2021-02-25 22:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0012_auto_20210224_0438'),
    ]

    operations = [
        migrations.AddField(
            model_name='themefieldoptions',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
