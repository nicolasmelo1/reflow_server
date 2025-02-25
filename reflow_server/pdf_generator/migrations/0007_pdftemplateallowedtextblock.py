# Generated by Django 3.1.4 on 2021-01-27 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rich_text', '0019_auto_20210127_1315'),
        ('pdf_generator', '0006_pdfgenerated'),
    ]

    operations = [
        migrations.CreateModel(
            name='PDFTemplateAllowedTextBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rich_text.textblocktype')),
            ],
            options={
                'db_table': 'pdf_template_allowed_text_block',
            },
        ),
    ]
