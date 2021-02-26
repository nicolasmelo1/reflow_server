# Generated by Django 3.1.4 on 2021-02-25 23:52

from django.db import migrations

import uuid


def migrate_add_uuid_to_field_options(apps, schema_editor):
    FieldOptions = apps.get_model('formulary', 'FieldOptions')

    for field_option in FieldOptions.objects.all():
        field_option.uuid = uuid.uuid4()
        field_option.save()

class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0003_fieldoptions_uuid'),
    ]

    operations = [
        migrations.RunPython(migrate_add_uuid_to_field_options)
    ]
