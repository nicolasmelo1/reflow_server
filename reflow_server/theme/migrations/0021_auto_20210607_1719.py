# Generated by Django 3.1.4 on 2021-06-07 17:19

from django.db import migrations
import re


def migrate_formula_variables_string_to_formula_variables_table(apps, schema_editor):
    ThemeFormulaVariable = apps.get_model('theme', 'ThemeFormulaVariable')
    ThemeField = apps.get_model('theme', 'ThemeField')

    fields_with_formulas = ThemeField.objects.filter(formula_configuration__isnull=False).exclude(formula_configuration='')
    for field in fields_with_formulas:
        variables = re.findall(r'{{\d+}}', field.formula_configuration, re.IGNORECASE)
        for index, variable in enumerate(variables):
            field_id = variable.replace(r'{{', '').replace(r'}}', '')
            if field_id.isdigit():
                variable_instance = ThemeField.objects.filter(id=int(field_id)).first()
                if variable_instance:
                    ThemeFormulaVariable.objects.create(field=field, variable=variable_instance, order=index)


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0020_themeformulavariable'),
    ]

    operations = [
        migrations.RunPython(migrate_formula_variables_string_to_formula_variables_table)
    ]
