# Generated by Django 3.1.4 on 2021-05-14 15:59
from django.db import migrations

import uuid

def migrate_add_uuid_to_dynamic_form(apps, schema_editor):
    DynamicForm = apps.get_model('data', 'DynamicForm')

    for dynamic_form in DynamicForm.objects.all():
        dynamic_form.uuid = uuid.uuid4()
        dynamic_form.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_dynamicform_uuid'),
    ]

    operations = [
        migrations.RunPython(migrate_add_uuid_to_dynamic_form)
    ]
