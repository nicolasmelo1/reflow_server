from django.conf import settings
from django.db import models

from reflow_server.formulary.models.abstract import AbstractForm, AbstractField, AbstractFieldOptions
from reflow_server.theme.managers import FormThemeManager, FieldOptionsThemeManager, FieldThemeManager, FormAccessedByThemeManager
from reflow_server.pdf_generator.managers import FormPDFGeneratorManager, FieldPDFGeneratorManager
from reflow_server.kanban.managers import FieldOptionsKanbanManager, OptionAccessedByKanbanManager
from reflow_server.formulary.managers import PublicAccessFieldFormularyManager, FormFormularyManager
from reflow_server.data.managers import FormDataManager, FieldDataManager, PublicAccessFieldDataManager


class SectionType(models.Model):
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
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'form_type'
        app_label = 'formulary'
        ordering = ('order',)


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
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'field_period_interval_type'
        app_label = 'formulary'
        ordering = ('order',)


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

    - The user saves a formulary that contains a `number` `field_type` that is formated as `percentage` (`percentage` format has base 100)
    - This number when it is saved to our database it is multiplied by DEFAULT_BASE_NUMBER_FIELD_FORMAT so `number*DEFAULT_BASE_NUMBER_FIELD_FORMAT`
    - Then we devide the multiplied number by the number format base. So if the user typed 70,00% in the front end, with basic math skills
    you know 70% means 0,7. So we devide the number he typed for the base (that for `percentage` is 100)

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
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'conditional_type'
        ordering = ('order',)
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
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'field_type'
        app_label = 'formulary'
        ordering = ('order',)

#############
#           #
#   BUILD   #
# FORMULARY #
#           #
#############

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
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    enabled = models.BooleanField(default=False)
    order = models.BigIntegerField()

    class Meta:
        ordering = ('order',)
        db_table = 'group'


class Form(AbstractForm):
    #TODO: Create a section model, for sections
    """
    Check reflow_server.formulary.models.abstract.AbstractForm for further explanation.

    This model defines two things: Formularies and Sections. We needed to configure it this way in order to create dynamic formsets.
    Okay, formularies are defined if depends_on is None, if depends_on is not None it is probably a section.

    Your conditionals can only be defined in sections, not on formularies. it doesn't make much sense on formularies.

    `company` field can be deleted since it is defined on the group.
    """
    depends_on = models.ForeignKey('self', models.CASCADE, null=True, blank=True, db_index=True,
                                   related_name='depends_on_form')
    enabled = models.BooleanField(default=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    conditional_on_field = models.ForeignKey('formulary.Field', models.SET_NULL, null=True, blank=True,
                                             related_name='conditional_on_field', db_index=True)
    group = models.ForeignKey(Group, models.CASCADE, db_index=True, null=True, related_name='form_group')

    class Meta:
        db_table = 'form'
        ordering = ('order',)

    objects = models.Manager()
    formulary_ = FormFormularyManager()
    theme_ = FormThemeManager()
    pdf_generator_ = FormPDFGeneratorManager()
    data_ = FormDataManager()


class Field(AbstractField):
    """
    Check reflow_server.formulary.models.abstract.AbstractField for further explanation.

    This model defines each field in the SECTION. If you haven't got it yet the order is: Group > Form > Section > Field
    I think this is kind of self explanatory, but this is the model that defines each field inside of a formulary.

    `form_field_as_otion` - This is used when the `field_type` is `form`. It means: use the data inserted of this field
    as the option for the user to select. So with this a user can connect a formulary with another and use the data inserted
    in a field of a formulary as the options displayed on another field.

    References:
    reflow_server.formulary.models.abstract.AbstractFieldOption
    reflow_server.formulary.models.FieldType
    reflow_server.formulary.models.FieldPeriodIntervalType
    reflow_server.formulary.models.FieldNumberFormatType
    reflow_server.formulary.models.FieldDateFormatType
    """
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True, related_name='form_fields')
    enabled = models.BooleanField(default=True, db_index=True)
    # this is actually a field state
    form_field_as_option = models.ForeignKey('self', models.SET_NULL, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'field'
        ordering = ('order',)
        app_label = 'formulary'

    objects = models.Manager()
    theme_ = FieldThemeManager()
    pdf_generator_ = FieldPDFGeneratorManager()
    data_ = FieldDataManager()


class FieldOptions(AbstractFieldOptions):
    """
    Check reflow_server.formulary.models.abstract.AbstractFieldOptions for further explanation.

    When the field_type is of type `option` or `multi-option`, we need to define some options for the field. 
    (kinda obvious) We define this here.
    """
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True, related_name='field_option')
    
    class Meta:
        db_table = 'field_options'
        ordering = ('order',)
        app_label = 'formulary'
    
    objects = models.Manager()
    theme_ = FieldOptionsThemeManager()
    kanban_ = FieldOptionsKanbanManager()
    

class OptionAccessedBy(models.Model):
    """
    This model is used to filter the options defined in reflow_server.formulary.models.FieldOptions that a user have access to

    You can check reflow_server.authentication.models.ProfileType for further explanation about profiles.

    So for example:

    If a user has a formulary with 3 fields: Status, Company Location and Client Name, and each of them being of the type `option`.
    When we create or update the user we can define a filter, the filter is as simple as: 
    "Which of the following options the user has access to?"

    This filter than does more than just display the options that a user has access to when he opens the formulary but it also
    filters only the formularies that have the option defined if he is a coordinator or an admin.

    So in the example i said above:
    - If Status have the following options: 'Negotiation Open', 'Negotiation Closed', 'Negotiating'
    - If the user A have access to the options:  'Negotiation Open' and 'Negotiating'
    - If user A is `admin` or `coordinator` on the listing and kanban he can view, or update the data of all 
    formularies that is filled with 'Negotiation Open' and 'Negotiating'. He WILL NOT be able to see data that
    was filled with 'Negotiation Closed'

    BY DEFAULT WHEN YOU CREATE A NEW OPTION ON THE FIELD ALL THE USERS HAVE ACCESS TO THIS FIELD, WHEN YOU CREATE A NEW USER, ALL
    THE NEW USER WILL HAVE ACCESS TO ALL FORMULARIES
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    field_option = models.ForeignKey('formulary.FieldOptions', models.CASCADE, db_index=True, related_name='option_accessed_by')
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, related_name='option_accessed_by_user')

    class Meta:
        db_table = 'option_accessed_by'
        app_label = 'formulary'

    objects = models.Manager()
    kanban_ = OptionAccessedByKanbanManager()


class FormAccessedBy(models.Model):
    """
    This works the same way as reflow_server.formulary.models.OptionAccessedBy but on formulary level.

    This defines which formularies a user has access to.

    If a company has formularies for the Finance and Sales teams respectively, than if the user B is from the Sales team
    he then doesn't have to have access to Finance formularies, only Sales. With this model we can filter the formularies
    the user has access to.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, related_name='form_accessed_by_user')

    class Meta:
        db_table = 'form_accessed_by'
        app_label = 'formulary'

    objects = models.Manager()
    theme_ = FormAccessedByThemeManager()


class PublicAccessForm(models.Model):
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    public_access = models.ForeignKey('authentication.PublicAccess', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'public_access_form'   


class PublicAccessField(models.Model):
    public_form = models.ForeignKey('formulary.PublicAccessForm', models.CASCADE, db_index=True)
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    public_access = models.ForeignKey('authentication.PublicAccess', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'public_access_field'   
    
    objects = models.Manager()
    formulary_ = PublicAccessFieldFormularyManager()
    data_ = PublicAccessFieldDataManager()