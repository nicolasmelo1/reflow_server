# Generated by Django 3.2.5 on 2021-11-22 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0026_alter_field_formula_configuration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='number_configuration_mask',
        ),
    ]
