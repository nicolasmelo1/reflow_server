# Generated by Django 3.2.5 on 2021-10-11 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_extractfiledata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formvalue',
            name='formula_configuration',
            field=models.TextField(blank=True, null=True),
        ),
    ]
