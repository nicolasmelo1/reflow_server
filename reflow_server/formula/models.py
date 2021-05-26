from django.db import models


class FormulaContextForCompany(models.Model):
    company = models.OneToOneField('authentication.Company', on_delete=models.CASCADE, db_index=True)
    context_type = models.ForeignKey('formula.FormulaContextType', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'formula_context_for_company'


class FormulaContextType(models.Model):
    language = models.CharField(max_length=280)
    name = models.CharField(max_length=280)
    order = models.IntegerField(default=1)

    class Meta:
        db_table = 'formula_context_type'
        ordering = ('order',)


class FormulaAttributeType(models.Model):
    name = models.CharField(max_length=280)
    order = models.IntegerField(default=1)

    class Meta:
        db_table = 'formula_attribute_type'
        ordering = ('order',)


class FormulaContextAttributeType(models.Model):
    context_type = models.ForeignKey('formula.FormulaContextType', on_delete=models.CASCADE, db_index=True, related_name='formula_context_type_attributes')
    attribute_type = models.ForeignKey('formula.FormulaAttributeType', on_delete=models.CASCADE, db_index=True, related_name='formula_context_type_attributes')
    translation = models.TextField()

    class Meta:
        db_table = 'formula_context_attribute_type'

