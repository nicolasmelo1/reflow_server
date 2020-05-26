from django.db import models


class FormType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This holds each type of the form
    This is actually for SECTIONS not for FORMS, we need to rename it later.

    There are 2 form types right now:
    - `form` - Is a single section, it works like a normal section of the Google Forms would be. So a single section that contains
    some fields
    - `multi-form` - This is kinda tricky, but it works like a single section also, at least how you build it, but it has one main 
    difference: the user can add more copy this section multiple times. 

    To understand better lets put in perspective with a simple formulary for sales. For this example we need to build a formulary like:
    - Some general information about the sales.
    - The history of each step on the sale.

    We need this in a single and unique formulary. For the first you might have a `form` type section, so it is single and unique for 
    the sale.

    The other is the history for the sale, your sale can consist of many e-mails, phone calls, and etc that must be documented.
    This section might contain fields like the `history_description` and `history_date`. On this example it can be a `multi-form`
    As a `multi-form` the user can add or delete as many history as he wants. Each one of the history will contain a the fields he defined
    within the section.
    """
    type = models.CharField(max_length=150, db_index=True)
    label_name = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'form_type'
        app_label = 'formulary'


class FieldPeriodIntervalType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model contains data that is used
    for `reflow_server.formulary.models.Field` that is a `period` `field_type`. So this contains the data that MUST be defined
    if the type of the field is `period`. This just tell us how to format the field if it is `period` `field_type`.

    As default, we always save data from this field as seconds. This way we can make calculus in the database and in this application
    easier because we then only work with real integer numbers. When we want to display a data to a user we convert it to 
    the desired format.
    """
    type = models.CharField(max_length=200, db_index=True)
    label_name = models.CharField(max_length=250)
    in_seconds = models.BigIntegerField()

    class Meta:
        db_table = 'field_period_interval_type'
        app_label = 'formulary'


class FieldNumberFormatType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model contains data that is used
    for `reflow_server.formulary.models.Field` that is a `number` `field_type`. So this contains the data that MUST be defined
    if the type of the field is `number`. This just tell us how to format the field if it is `number` `field_type`.

    As default, we always save data from this field as integer. This way we can make calculus in the database and in this application
    easier because we then only work with real integer numbers. When we want to display a data to a user we convert it to 
    the desired format.

    With the information above you might be wondering: BUT HEY, HOW DO YOU WORK WITH FRACTIONS LIKE 0,98 or PERCENTAGES?

    For this you need to see the settings.py defined in the root of this django project for the DEFAULT_BASE_NUMBER_FIELD_FORMAT and
    DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION.

    Every number saved on the database wheater it has a decimal defined or not is multiplied by the number defined on the 
    DEFAULT_BASE_NUMBER_FIELD_FORMAT setting. This means, the maximum number of decimal places accepted for for numbers 
    is the number of `0` in this default number.

    For percentages we use the "base" field of this model. This is the number that we devides to when we display a number to the user.
    So let's understand with this example:

    1 - The user saves a formulary that contains a `number` `field_type` that is formated as `percentage` (`percentage` format has base 100)
    2 - This number when it is saved to our database it is multiplied by DEFAULT_BASE_NUMBER_FIELD_FORMAT so `number*DEFAULT_BASE_NUMBER_FIELD_FORMAT`
    3 - Then we devide the multiplied number by the number format base. So if the user typed 70,00% in the front end, with basic math skills
    you know 70% means 0,7. So we devide the number he typed for the base (that for percentage is 100)

    Then when we display the number for the user we do the same thing but in the opposite order.

    - `prefix` is what comes before the number.
    - `suffix` is a string that comes after the number.
    - `thousand_separator` is a string containing how you want to separate thousands. For brazilians it is `.`, for americans
    it might be ','
    - `decimal_separator` same as above, some countries separate decimals using `.`
    - `precision` the maximum precision of this format. For monetary you might want to display only two decimal places before the `,`.
    """
    type = models.CharField(max_length=200, db_index=True)
    label_name = models.CharField(max_length=250)
    precision = models.BigIntegerField(default=1)
    prefix = models.CharField(max_length=250, null=True)
    suffix = models.CharField(max_length=250, null=True)
    thousand_separator = models.CharField(max_length=10, null=True)
    decimal_separator = models.CharField(max_length=10, null=True)
    order = models.BigIntegerField()
    base = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'field_number_format_type'
        ordering = ('order',)
        app_label = 'formulary'


class FieldDateFormatType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model contains data that is used
    for `reflow_server.formulary.models.Field` that is a `date` `field_type`. So this contains the data that MUST be defined
    if the type of the field is `date`. This just tell us how to format the field if it is `date` `field_type`.

    The format follows python datetime guidelines, so if you want to display a date with formatted as the `MM-YY` 
    you need to create here a formatter for this type of date. 
    Since this follows python datetime guidelines in this example you would create a new row with the following format 
    `%m-%y`.

    Using python datetime guideline can be kind of tricky specially if the user working doesn't have fluency in python.
    For this you can change this to follow ISO 8601 (don't forget to change everything regarding to date if you make this change)
    also the frontend.

    Okay, so with this you understand how date formatting works in our system, but we usually need this field type to send 
    notifications or do other works in our system, so all of the `date` `field_type` that is saved in your database must
    follow a default and same rule regardless of the formatting it has. For it you might want to check 
    `DEFAULT_DATE_FIELD_FORMAT` setting in `settings.py`.

    The `DEFAULT_DATE_FIELD_FORMAT` defines the default date format, so even if the user wants to saves only the year of 
    the date, we need to format it with the following format, containing month, day and even hour, second and minutes.
    """
    type = models.CharField(max_length=200, db_index=True)
    label_name = models.CharField(max_length=250)
    format = models.CharField(max_length=250)
    order = models.BigIntegerField()

    class Meta:
        db_table = 'field_date_format_type'
        ordering = ('order',)
        app_label = 'formulary'


class ConditionalType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds the default data used for conditional sections
    Conditional sections are sections that are displayed on the formulary when a condition equals to True. But a conditional can be many types:
    - Greater than Value
    - Less than Value
    - Equal to Value
    - Different than Value
    With this model we define the type for a condition, right now we only have Equal.
    """
    type = models.CharField(max_length=150, db_index=True)
    label_name = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'conditional_type'
        app_label = 'formulary'


class FieldType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. I think it doesn't need much explaining, 
    since it got many explanations in many models for each field type.

    So with this a important thing to say is: IT IS REALLY IMPORTANT TO BE CAREFULL WHEN REMOVING OR ADDING A FIELD TYPE.

    References:
    reflow_server.formulary.models.abstract.AbstractFieldOption
    reflow_server.formulary.models.FieldPeriodIntervalType
    reflow_server.formulary.models.FieldNumberFormatType
    reflow_server.formulary.models.FieldDateFormatType
    """
    type = models.CharField(max_length=200, db_index=True)
    label_name = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = 'field_type'
        app_label = 'formulary'


class Group(models.Model):
    """
    This might be tricky if you are user hahaha. Okay, so groups are called templates for the user, for us, developers,
    we separate the `Templates` in two categories: `Themes` and `Groups`. 
    
    Themes are defined better in the `themes` app. 
    Groups on the other hand are a group of formularies. So imagine the following example:
    - The user has created two forms for the Sales Team and three forms for the Development Team. How does he organize them?
    - He can organize them inside groups. So there will be two forms inside the `Sales` group and three forms in the `Development`
    group.
    - He can always rename them how the him wants.

    This has only one difference from `fields`, `sections` or `forms`, you can't create groups freely, they need to be created ONLY
    selecting a theme.
    """
    name = models.CharField(max_length=500)
    company = models.ForeignKey('auth.Company', models.CASCADE, db_index=True)
    enabled = models.BooleanField(default=False)
    order = models.BigIntegerField()

    class Meta:
        ordering = ('order',)
        db_table = 'group'


class Form(AbstractForm):
    """
    Check reflow_server.formulary.models.abstract.AbstractForm for further explanation.

    This model defines two things: Formularies and Sections. We needed to configure it this way in order to create dynamic formsets.
    Okay, formularies are defined if depends_on is None, if depends_on is not None it is probably a section.

    Your conditionals can only be defined in sections, not on formularies. it doesn't make much sense.

    `company` field can be deleted since it is defined on the group.
    """
    depends_on = models.ForeignKey('self', models.CASCADE, null=True, blank=True, db_index=True,
                                   related_name='depends_on_form')
    enabled = models.BooleanField(default=True)
    company = models.ForeignKey('auth.Company', models.CASCADE, db_index=True)
    conditional_on_field = models.ForeignKey('formulary.Field', models.SET_NULL, null=True, blank=True,
                                             related_name='conditional_on_field', db_index=True)
    group = models.ForeignKey(Group, models.CASCADE, db_index=True, null=True, related_name='form_group')

    class Meta:
        db_table = 'form'
        ordering = ('order',)


class Field(AbstractField):
    form = models.ForeignKey(Form, models.CASCADE, db_index=True, related_name='form_fields')
    enabled = models.BooleanField(default=True, db_index=True)
    # this is actually a field state
    form_field_as_option = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'field'
        ordering = ('order',)
        app_label = 'data'


class FieldOptions(AbstractFieldOptions):
    field = models.ForeignKey(Field, models.CASCADE, db_index=True, related_name='field_option')
    
    class Meta:
        db_table = 'field_options'
        ordering = ('order',)
        app_label = 'data'


class OptionAccessedBy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    field_option = models.ForeignKey(FieldOptions, models.CASCADE, db_index=True, related_name='option_accessed_by')
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True, related_name='option_accessed_by_user')

    class Meta:
        db_table = 'option_accessed_by'
        app_label = 'data'


class FormAccessedBy(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    form = models.ForeignKey(Form, models.CASCADE, db_index=True)
    user = models.ForeignKey(UserExtended, models.CASCADE, db_index=True, related_name='form_accessed_by_user')

    class Meta:
        db_table = 'form_accessed_by'
        app_label = 'data'
