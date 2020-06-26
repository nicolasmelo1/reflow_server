from django.db import models


class AggregationType(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'aggregation_type'


class ChartType(models.Model):
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'chart_type'


class DashboardChartConfiguration(models.Model):
    name = models.CharField(max_length=350)
    for_company = models.BooleanField(default=False)
    aggregation_type = models.ForeignKey('dashboard.AggregationType', on_delete=models.CASCADE, db_index=True,
                                         related_name='dashboard_chart_configuration_aggregation_types')
    chart_type = models.ForeignKey('dashboard.ChartType', on_delete=models.CASCADE, db_index=True,
                                    related_name='dashboard_chart_configuration_chart_types')
    number_format_type = models.ForeignKey('formulary.FieldNumberFormatType', on_delete=models.CASCADE, db_index=True,
                                            related_name='dashboard_chart_configuration_number_format_types')
    label_field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, db_index=True, 
                                    related_name='dashboard_chart_configuration_label_fields')
    value_field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, db_index=True,
                                    related_name='dashboard_chart_configuration_value_fields')
    form = models.ForeignKey('formulary.Form', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, db_index=True, 
                             related_name='dashboard_chart_configuration_users')
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, db_index=True,
                                related_name='dashboard_chart_configuration_companies')
    class Meta:
        db_table = 'dashboard_chart_configuration'
