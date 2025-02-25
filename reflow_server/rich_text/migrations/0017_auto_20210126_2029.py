# Generated by Django 3.1.4 on 2021-01-26 20:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rich_text', '0016_textimageoption_file_image_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='texttableoption',
            name='columns_num',
        ),
        migrations.RemoveField(
            model_name='texttableoption',
            name='rows_num',
        ),
        migrations.CreateModel(
            name='TextTableOptionRowDimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.BigIntegerField(default=None, null=True)),
                ('text_table_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_table_option_row_dimensions', to='rich_text.texttableoption')),
            ],
            options={
                'db_table': 'text_table_option_row_dimension',
            },
        ),
        migrations.CreateModel(
            name='TextTableOptionColumnDimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.BigIntegerField(default=None, null=True)),
                ('text_table_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_table_option_column_dimensions', to='rich_text.texttableoption')),
            ],
            options={
                'db_table': 'text_table_option_column_dimension',
            },
        ),
    ]
