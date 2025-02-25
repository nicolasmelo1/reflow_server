# Generated by Django 3.1 on 2020-10-16 19:42

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0006_migrate_company_to_theme'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='themedashboardchartconfiguration',
            managers=[
                ('theme_', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='theme',
            name='theme_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='theme_theme_type', to='theme.themetype'),
        ),
    ]
