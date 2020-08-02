from django.db import models

class FormulaType(models.Model):
    """
    This model holds all of the possible formulas. Formulas are actually classes we define in
    the file define in FORMULA_FORMULAS in settings.py file. This setting is used to check for
    classes used inside of the file.

    What does classes do is make calculations. When we use a formula like SUM, or COUNT we actually
    want to make a calculation, we use the values inside `()` and separated by `;` as parameters for
    the calculation.

    Okay, so why this class. We could also use the classes directly, if it we can activate and deactivate
    a formula just changing the database and without even needing to touch the code. It's important
    to understand only that `name` here should be always upper case, and must conform with the same names
    of the formulas already created in the FORMULA_FORMULAS file.
    """
    name = models.CharField(max_length=50)
    label_name = models.CharField(max_length=100)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'formula_type'
        ordering = ('order',)