from django.db import models


class FilterConditionalType(models.Model):
    name = models.CharField(max_length=280)
    order = models.IntegerField(null=True)

    class Meta:
        db_table = 'filter_conditional_type'
        ordering = ('order',)


class FilterConectorType(models.Model):
    name = models.CharField(max_length=280)
    order = models.IntegerField(null=True)

    class Meta:
        db_table = 'filter_conector_type'
        ordering = ('order',)


class FilterConditionalTypeByFieldTypeType(models.Model):
    filter_conditional_type = models.ForeignKey('filter.FilterConditionalType', on_delete=models.CASCADE)
    field_type = models.ForeignKey('formulary.FieldType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'filter_conditional_type_by_field_type_type'


class Filter(models.Model):
    """
    Responsible for filtering data and matching conditions for a particular company and for a particular formulary.
    The idea is simple. With filters we can make conditions, those conditions can work on a single record or on a bunch of records.
    This means that with filters we can actually filter the data or try to match conditionals like check if a conditional section
    needs to be open or not.

    This way it becomes a lot easier to reuse conditionals in many places of the application, search through each conditionals and so on.
    
    Okay so you might ask:
    why is it not in data? Data is already bloated with handling too much stuff. Since we needed to add new tables and do other stuff we decided to keep it
    outside of this app.
    Also, for handling conditions like filtering a bunch of data this might makes sense to add there. But for stuff like handling a single record this might 
    not make any sense.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    form = models.ForeignKey('formulary.Form', on_delete=models.CASCADE, related_name='form_filters')
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='company_filters')
    
    class Meta:
        db_table = 'filter'


class FilterCondition(models.Model):
    filter = models.ForeignKey('filter.Filter', on_delete=models.CASCADE, related_name='filter_condition_filter')
    field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, related_name='filter_condition_user')
    is_negation = models.BooleanField(default=False)
    conditional_type = models.ForeignKey('filter.FilterConditionalType', on_delete=models.CASCADE)
    value = models.CharField(max_length=1000, blank=True)
    value2 = models.CharField(max_length=1000, blank=True, null=True)
    conector_type = models.ForeignKey('filter.FilterConectorType', on_delete=models.CASCADE, null=True)
    order = models.IntegerField()

    class Meta:
        db_table = 'filter_condition'
        ordering = ('order',)