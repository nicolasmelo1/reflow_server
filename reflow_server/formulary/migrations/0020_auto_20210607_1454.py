# Generated by Django 3.1.4 on 2021-06-07 14:54

from django.db import migrations, models
import re


def migrate_formula_variables_string_to_formula_variables_table(apps, schema_editor):
    FormulaVariable = apps.get('formulary', 'FormulaVariable')
    Field = apps.get_model('formulary', 'Field')

    fields_with_formulas = Field.objects.filter(formula_configuration__isnull=False).exclude(formula_configuration='')
    for field in fields_with_formulas:
        variables = re.findall(r'{{\d+}}', fields_with_formulas.formula_configuration, re.IGNORECASE)
        for index, variable in enumerate(variables):
            field_id = variable.replace(r'{{', '').replace(r'}}', '')
            if field_id.isdigit():
                variable_instance = Field.objects.filter(id=int(field_id)).first()
                if variable_instance:
                    FormulaVariable.objects.create(field=field, variable=variable_instance, order=index)


class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0019_formulavariable'),
    ]

    operations = [
        migrations.RunPython(migrate_formula_variables_string_to_formula_variables_table)
    ]
