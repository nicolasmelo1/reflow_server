# Generated by Django 3.1.4 on 2021-01-07 14:57

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('rich_text', '0011_auto_20210106_1651'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='textimageoption',
            managers=[
                ('rich_text_', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='textimageoption',
            name='link',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
