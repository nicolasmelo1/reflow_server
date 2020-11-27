# Generated by Django 3.1 on 2020-11-26 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rich_text', '0006_auto_20201126_1627'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formulary', '0002_auto_20200719_1720'),
        ('authentication', '0010_auto_20200902_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFTemplateConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=500)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.company')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulary.form')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pdf_template_configuration',
            },
        ),
        migrations.CreateModel(
            name='PDFTemplateConfigurationVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulary.field')),
                ('pdf_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='template_configuration_variables', to='pdf_generator.pdftemplateconfiguration')),
            ],
            options={
                'db_table': 'pdf_template_configuration_variables',
            },
        ),
        migrations.CreateModel(
            name='PDFTemplateConfigurationRichText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_template', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pdf_template_rich_text', to='pdf_generator.pdftemplateconfiguration')),
                ('rich_text', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rich_text_pdf_template', to='rich_text.textpage')),
            ],
            options={
                'db_table': 'pdf_template_configuration_rich_text',
            },
        ),
    ]
