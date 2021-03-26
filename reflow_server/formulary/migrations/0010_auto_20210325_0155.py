# Generated by Django 3.1.4 on 2021-03-25 01:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0009_defaultfieldvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultFieldValueAttachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.CharField(blank=True, max_length=500, null=True)),
                ('bucket', models.CharField(default='reflow-crm', max_length=200)),
                ('file_attachments_path', models.CharField(default='default-file-attachments', max_length=250)),
                ('file_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('file_size', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'default_attachments',
            },
        ),
        migrations.AddField(
            model_name='defaultfieldvalue',
            name='default_attachment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='formulary.defaultfieldvalueattachments'),
        ),
    ]
