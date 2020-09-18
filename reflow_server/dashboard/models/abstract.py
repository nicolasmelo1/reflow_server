from django.db import models


class AbstractDashboardChartConfiguration(models.Model):
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
    aggregation_type = models.ForeignKey('dashboard.AggregationType', on_delete=models.CASCADE, db_index=True)
    chart_type = models.ForeignKey('dashboard.ChartType', on_delete=models.CASCADE, db_index=True)
    number_format_type = models.ForeignKey('formulary.FieldNumberFormatType', on_delete=models.CASCADE, db_index=True)
    
    class Meta:
        abstract = True
