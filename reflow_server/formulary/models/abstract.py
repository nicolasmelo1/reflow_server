from django.db import models

import uuid


class AbstractFormulaVariable(models.Model):
    order = models.BigIntegerField()

    class Meta:
        abstract = True


class AbstractForm(models.Model):
    """
    This is the abstract for Forms (do not mistake with DynamicForm), this abstract is used to define
    Forms, forms are a mix of sections, and within each section some fields. Right now Sections are defined with this
    model also. Each object that has depends_on = None is a formulary, each object that has depends_on not None is a section.
    
    I know it is confusing but it was required when we were dependending on django Formsets to create formularies, now we don't
    need it anymore, so it can be changed.

    It is important to understand that `form_name` works like `name` in `reflow_server.formulary.models.Fields`. It is a field
    that works like a slug for that formulary. It NEEDS to be unique for EACH COMPANY, not for the hole system. Usually 
    this field does not accept any special characters, ponctuations or spaces since it needs to work well on urls or JSON objects.

    Conditionals are only set on sections right now, not on formularies but it is important to understand
    how it works (we want to move it from being bound to sections to become a unique app that can handle
    other conditionals, like on notifications, on filters and etc)
    We define 3 things on conditionals:
    - conditional_type - right now just `equal`, so how to handle the conditionals
    - conditional_value - the value to verify, checks if the value of a field matches the string defined here
    - conditional_on_field - the field to consider for this conditional, so when this field has a specific
                             `conditional_value`

    With the conditionals we have 2 important logics: 
    - When the conditional is set, a required field SHOULD be required
    - When the conditional is not set, the data from the conditional section (if it has any) MUST be deleted.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    form_name = models.CharField(max_length=150, db_index=True)
    label_name = models.CharField(max_length=150)
    uuid = models.UUIDField(default=uuid.uuid4)
    type = models.ForeignKey('formulary.SectionType', models.CASCADE, db_index=True)
    order = models.BigIntegerField()
    conditional_type = models.ForeignKey('formulary.ConditionalType', models.CASCADE, null=True, blank=True, db_index=True)
    conditional_value = models.CharField(max_length=200, null=True, blank=True)
    show_label_name = models.BooleanField(default=True)
    conditional_excludes_data_if_not_set = models.BooleanField(default=True)

    class Meta:
        abstract = True
        app_label = 'formulary'


class AbstractFieldStates(models.Model):
    """
    THIS MODEL IS IMPORTANT AND CONTAINS SOME IMPORTANTE BUSINESS RULES

    So this abstract model is actually for saving the state of the field inside of the 
    `data.models.FormValue` model and on `formulary.models.Field` model.

    This model contains the `FieldStates` string in its name because it is used to hold the State of 
    the field of the data that was saved.

    If you ever used Airtable or other dynamic database creation programs, or even a simple Postgres database
    you will notice a similar behaviour with them, this behaviour is:
    Like a database, if the user change a column type, all of the items in the column should change the
    type too, requiring some kind of migration. 
    We don't work this way, we work more like a NoSQL database. If a user change the type of the field
    or many other configurations of a field the data he saved before the change is preserved with its state.

    This way we prevent the user from loosing important data when he changes something in the formulary.

    Although the data is safe, some stuff like ordering or searching through your data might not return 
    some old values.
    """
    date_configuration_date_format_type = models.ForeignKey('formulary.FieldDateFormatType', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    period_configuration_period_interval_type = models.ForeignKey('formulary.FieldPeriodIntervalType', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    number_configuration_mask = models.CharField(max_length=250, blank=True, null=True) # Needs to be removed
    number_configuration_number_format_type = models.ForeignKey('formulary.FieldNumberFormatType', on_delete=models.CASCADE, blank=True, null=True, db_index=True)
    formula_configuration = models.TextField(blank=True, null=True)
    is_long_text_rich_text = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        abstract = True
        app_label = 'formulary'


class AbstractField(AbstractFieldStates):
    """
    As it was explained earlier, in the AbstractForm, a formulary is a composition of Section and fields within a section.

    This abstract is for defining the field. Also as i said earlier, it inherits from AbstractFieldStates because it must 
    contain the state of the field. (This might be kinda obvious but anyway)

    It is important to understand that `name` works like `form_name` in `reflow_server.formulary.models.Form`. It is a field
    that works like a slug for that formulary. It NEEDS to be unique for EACH COMPANY, not for the hole system. Usually 
    this field does not accept any special characters, ponctuations or spaces since it needs to work well on urls or JSON objects.
    Usually is this what we show to the user when adding variables to text in the notification or formulas. Again, it's important
    to understand this MUST BE UNIQUE for the hole company. So you can have more than one company sharing the same name of a field.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=300, db_index=True)
    label_name = models.CharField(max_length=300, blank=True, null=True)
    placeholder = models.CharField(blank=True, null=True, max_length=450)
    required = models.BooleanField(default=True)
    order = models.BigIntegerField()
    uuid = models.UUIDField(default=uuid.uuid4)
    is_unique = models.BooleanField(default=False)
    field_is_hidden = models.BooleanField(default=False)
    label_is_hidden = models.BooleanField(default=False)
    date_configuration_auto_create = models.BooleanField(default=False)
    date_configuration_auto_update = models.BooleanField(default=False)
    number_configuration_allow_negative = models.BooleanField(default=True)
    number_configuration_allow_zero = models.BooleanField(default=True)
    # this is actually a field state
    type = models.ForeignKey('formulary.FieldType', models.CASCADE, db_index=True)


    class Meta:
        abstract = True
        app_label = 'formulary'


class AbstractFieldOptions(models.Model):
    """
    This simple abstract model is used for holding the Field Option. The Field as you know has many `types`. It can be a `option`,
    a `multi-option`, a `form`, `text`, `number`, etc. For `option` and `multi-option` we use this model here to store
    all of the options of a field.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    option = models.CharField(max_length=500, db_index=True)
    order = models.BigIntegerField()
    uuid = models.UUIDField(default=uuid.uuid4)

    class Meta:
        abstract = True


class AbstractDefaultFieldValue(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    value = models.TextField()

    class Meta:
        abstract = True