# Generated by Django 3.1 on 2020-12-03 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rich_text', '0008_auto_20201202_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='textcontent',
            name='text_size',
            field=models.IntegerField(default=12),
        ),
    ]
