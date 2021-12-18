from django.db import models

from reflow_server.dashboard.models.abstract import AbstractDashboardChartConfiguration
from reflow_server.theme.managers import DashboardChartConfigurationThemeManager
from reflow_server.dashboard.managers import DashboardChartConfigurationDashboardManager


class AggregationType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds the type of aggregation,
    so could be `sum`, `count`, `average` and others. This might be really straight forward so no further explanation required.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'aggregation_type'
        ordering = ('order',)


class ChartType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds all the possible charts
    a user can create, so they can be `pie`, `bar` and so on. It's important to understand that charts are not only the graphs 
    (the ones you usually draw) but can be other types like a card of totals and so on. 
    What this means is, wathever way you want to display the aggregated data the type should be defined here.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'chart_type'
        ordering = ('order',)


class DashboardChartConfiguration(AbstractDashboardChartConfiguration):
    """
    For further explanation on what this model do read reflow_server.dashboard.models.AbstractDashboardConfiguration.

    In the most basic sense, this is used for holding the dashboard configuration data needed to construct the dashboards.
    IT DOES NOT HOLD THE DATA AGGREGATED DATA, BUT THE DATA NEEDED TO BUILD THE CHARTS.
    """
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

    objects = models.Manager()
    theme_ = DashboardChartConfigurationThemeManager()
    dashboard_ = DashboardChartConfigurationDashboardManager()