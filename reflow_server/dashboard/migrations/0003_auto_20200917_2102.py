# Generated by Django 3.1 on 2020-09-17 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulary', '0002_auto_20200719_1720'),
        ('dashboard', '0002_auto_20200719_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardchartconfiguration',
            name='aggregation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.aggregationtype'),
        ),
        migrations.AlterField(
            model_name='dashboardchartconfiguration',
            name='chart_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.charttype'),
        ),
        migrations.AlterField(
            model_name='dashboardchartconfiguration',
            name='number_format_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulary.fieldnumberformattype'),
        ),
    ]
