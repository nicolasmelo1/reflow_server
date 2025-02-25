# Generated by Django 3.1.4 on 2021-06-07 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0019_themefield_is_long_text_rich_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeFormulaVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.BigIntegerField()),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formula_variable_theme_fields', to='theme.themefield')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='theme_field_formula_variable', to='theme.themefield')),
            ],
            options={
                'db_table': 'theme_formula_variable',
            },
        ),
    ]
