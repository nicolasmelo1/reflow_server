# Generated by Django 3.1.4 on 2021-05-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0019_fieldtype_is_dynamic_evaluated'),
    ]

    operations = [
        migrations.AddField(
            model_name='fieldnumberformattype',
            name='has_to_enforce_decimal',
            field=models.BooleanField(default=False),
        ),
    ]
