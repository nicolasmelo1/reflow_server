# Generated by Django 3.2.5 on 2021-10-18 22:47

from django.db import migrations
from django.db.models import Q

def migrate_connected_formulary_value_matching_to_form_instead_of_section(apps, schema_editor):
    FormValue = apps.get_model('data', 'FormValue')
    DynamicForm = apps.get_model('data', 'DynamicForm')

    all_form_field_type_values = FormValue.objects.filter(field_type__type='form')
    for form_field_type_value in all_form_field_type_values:
        hopefully_a_dynamic_form_section_id = form_field_type_value.value
        if hopefully_a_dynamic_form_section_id.isdigit():
            dynamic_form_section = DynamicForm.objects.filter(id=int(hopefully_a_dynamic_form_section_id)).first()
            if dynamic_form_section and dynamic_form_section.depends_on_id:
                form_field_type_value.value = str(dynamic_form_section.depends_on_id)
                form_field_type_value.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0009_alter_formvalue_formula_configuration'),
    ]

    operations = [
        migrations.RunPython(migrate_connected_formulary_value_matching_to_form_instead_of_section)

    ]
