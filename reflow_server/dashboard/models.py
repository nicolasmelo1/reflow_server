from django.db import models


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


class DashboardChartConfiguration(models.Model):
    """
    This model is responsible for holding each chart configuration. Each chart configuration is bound to a specific company,
    a specific user and a specific formulary. This means you can't have charts that cross information between formularies. 
    You can't aggregate a data from a another formulary to this formulary.

    To understand how this works you first need to understand what is an aggregation, in a simple explanation a aggregation 
    is actually kinda the same as a python dict. What this means is:
    1 - You first have the keys (labels)
    2 - Each key have a value (values)
    
    That's why we need label_field and value_field, to know which field from the formulary to use as keys, and which to use as
    value. This means that obviously to work with charts you need to work with charts you need to fill the formularies with data.
    
    Besides that a chart configuration should hold these informations:
    - How we want to aggregate the data
    - How we want to display the data to the user
    - How to format each number to the user on the result
    """
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
    #order = models.BigIntegerField(default=1)
    class Meta:
        db_table = 'dashboard_chart_configuration'
