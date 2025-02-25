# Generated by Django 3.0.6 on 2020-06-25 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0002_auto_20200608_1957'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formulary', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'aggregation_type',
            },
        ),
        migrations.CreateModel(
            name='ChartType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'chart_type',
            },
        ),
        migrations.CreateModel(
            name='DashboardChartConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=350)),
                ('for_company', models.BooleanField(default=False)),
                ('aggregation_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_aggregation_types', to='dashboard.AggregationType')),
                ('chart_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_chart_types', to='dashboard.ChartType')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_companies', to='authentication.Company')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formulary.Form')),
                ('label_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_label_fields', to='formulary.Field')),
                ('number_format_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_number_format_types', to='formulary.FieldNumberFormatType')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_users', to=settings.AUTH_USER_MODEL)),
                ('value_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_chart_configuration_value_fields', to='formulary.Field')),
            ],
            options={
                'db_table': 'dashboard_chart_configuration',
            },
        ),
    ]
