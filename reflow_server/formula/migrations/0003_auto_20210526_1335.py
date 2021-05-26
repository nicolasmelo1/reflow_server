# Generated by Django 3.1.4 on 2021-05-26 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_publicaccess'),
        ('formula', '0002_auto_20200719_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormulaAttributeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=280)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'formula_attribute_type',
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='FormulaContextAttributeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translation', models.TextField()),
                ('attribute_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formula_context_type_attributes', to='formula.formulaattributetype')),
            ],
            options={
                'db_table': 'formula_context_attribute_type',
            },
        ),
        migrations.CreateModel(
            name='FormulaContextForCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
            ],
            options={
                'db_table': 'formula_context_for_company',
            },
        ),
        migrations.CreateModel(
            name='FormulaContextType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=280)),
                ('name', models.CharField(max_length=280)),
                ('order', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'formula_context_type',
                'ordering': ('order',),
            },
        ),
        migrations.DeleteModel(
            name='FormulaType',
        ),
        migrations.AddField(
            model_name='formulacontextforcompany',
            name='context_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formula.formulacontexttype'),
        ),
        migrations.AddField(
            model_name='formulacontextattributetype',
            name='context_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='formula_context_type_attributes', to='formula.formulacontexttype'),
        ),
    ]
