from django.db import models


class FilterConditionalType(models.Model):
    name = models.CharField(max_length=280)

    class Meta:
        db_table = 'filter_conditional_type'


class FilterConectorType(models.Model):
    name = models.CharField(max_length=280)

    class Meta:
        db_table = 'filter_conector_type'


class Filter(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey('formulary.Form', on_delete=models.CASCADE, related_name='filter_form')
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='filter_company')
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, null=True, related_name='filter_user')
    class Meta:
        db_table = 'filter'


class FilterCondition(models.Model):
    filter = models.ForeignKey('filter.Filter', on_delete=models.CASCADE, related_name='filter_condition_filter')
    field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, related_name='filter_condition_user')
    conditional_type = models.ForeignKey('filter.FilterConditionalType', on_delete=models.CASCADE)
    value = models.CharField(max_length=1000, blank=True)
    conector_type = models.ForeignKey('filter.FilterConectorType', on_delete=models.CASCADE, null=True)
    order = models.IntegerField()

    class Meta:
        db_table = 'filter_condition'