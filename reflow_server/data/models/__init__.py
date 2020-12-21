from django.conf import settings
from django.db import models

from reflow_server.formulary.models.abstract import AbstractFieldStates

from reflow_server.data.managers import FormValueDataManager, AttachmentsDataManager, \
    DynamicFormDataManager
from reflow_server.notification.managers import FormValueNotificationManager
from reflow_server.kanban.managers import FormValueKanbanManager, \
    DynamicFormKanbanManager
from reflow_server.listing.managers import FormValueListingManager, \
    DynamicFormListingManager
from reflow_server.formulary.managers import FormValueFormularyManager
from reflow_server.formula.managers import FormValueFormulaManager, \
    DynamicFormFormulaManager
from reflow_server.pdf_generator.managers import FormValuePDFGeneratorManager, \
    DynamicFormPDFGeneratorManager, pdf_generated


class DynamicForm(models.Model):
    #TODO: Create a section model, for sections
    """
    TL:DR: While `reflow_server.formulary.models.Form` represents the data to BUILD the form, this represents the data
    of the Form

    This is the model that represents each formulary and section data. Yup, the data, and how to build the formulary
    are different from each other.

    This is explained well in the frontend. But we need to explain here also.

    This works kind of the same way as the `reflow_server.formulary.models.Form` works. Except the first has data containg
    HOW to build the formulary and here we have data that explain WHAT we build on the formulary. OKAY, WUT?

    Okay, think this way: Imagine we have a `multi-form` section called 'Historico'. This section when loaded for the user,
    is not loaded displaying the fields. Just a simple button to add a new Section. The WHAT here define how many `multi-forms`
    will be loaded. For further explanation you can check `Reflow Front` app inside the `shared/components/Formulary` read `ABOUT.md`

    Anyway, this works the same way as `reflow_server.formulary.models.Form` so when `depends_on` is None, it is a Form, 
    if `depends_on` is NOT None then it references a section.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.SET_NULL, db_index=True, blank=True, null=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True, blank=True, null=True, related_name='company_dynamic_form')
    depends_on = models.ForeignKey('self', models.CASCADE, blank=True, null=True, db_index=True,
                                   related_name='depends_on_dynamic_form')

    class Meta:
        db_table = 'dynamic_forms'
        ordering = ('-updated_at',)
        app_label = 'data'

    objects = models.Manager()
    data_ = DynamicFormDataManager()
    formula_ = DynamicFormFormulaManager()
    kanban_ = DynamicFormKanbanManager()
    listing_ = DynamicFormListingManager()
    pdf_generator_ = DynamicFormPDFGeneratorManager()


class FormValue(AbstractFieldStates):
    """
    This is actually a simple, and might be one of the biggest table of our database. Why? Because this represents
    the data for EACH field. Every value that the user fill on every formulary is saved as a string in our database,
    even options.

    Yup, this might not be really efficient, since we need to cast constantly for other formats.
    But this way we keep the data concise and simple to work.

    It's important to notice, sometimes a same field on the same section, might consume multiple rows on our database.
    This happens for `multi-options` `field_type`, if the user has selected more than one option in the formulary, each of the
    option he selected will be displayed in distinct row a single row. 

    This model also holds the state of the fields, you can read more about it on `reflow_server.formulary.models.abstract.AbstractFieldStates`
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True, blank=True, null=True, related_name='field_value')
    value = models.TextField(blank=True, null=True)
    form = models.ForeignKey('data.DynamicForm', models.CASCADE, db_index=True, blank=True, null=True,
                             related_name='dynamic_form_value')
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True, blank=True, null=True, related_name='company_value')
    # below here is actually info about the field state
    form_field_as_option = models.ForeignKey('formulary.Field', models.SET_NULL, blank=True, null=True, db_index=True)
    field_type = models.ForeignKey('formulary.FieldType', models.CASCADE, db_index=True, null=True, related_name='field_type_value')

    class Meta:
        db_table = 'form_value'
        app_label = 'data'

    objects = models.Manager()
    data_ = FormValueDataManager()
    listing_ = FormValueListingManager()
    kanban_ = FormValueKanbanManager()
    formulary_ = FormValueFormularyManager()
    formula_ = FormValueFormulaManager()
    notification_ = FormValueNotificationManager()
    pdf_generator_ = FormValuePDFGeneratorManager()


class Attachments(models.Model):
    """
    This model holds all of the attachments of a formulary.

    Right now attachments are saved on S3, but we could change it sometime in the near future. Because of this we use 
    this model to save stuff like:

    From which SECTION is this attachment referenced to? Okay, but from which Field on this section? What was the bucket 
    that this attachment was saved (if it has a bucket)? On which path? What is the size of the file? And what is the url to
    get the file?

    With this we can later change where we save attachments without facing much issues. Making migrations MUCH, MUCH easier.

    It is something that even Django Storages don't give us.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.CharField(max_length=500, null=True, blank=True)
    field = models.ForeignKey('formulary.Field', on_delete=models.CASCADE, blank=True, null=True, db_index=True,
                              related_name='field_attachment')
    form = models.ForeignKey('data.DynamicForm', on_delete=models.CASCADE, blank=True, null=True, db_index=True,
                             related_name='dynamic_form_attachment')
    bucket = models.CharField(max_length=200, default=settings.S3_BUCKET)
    file_attachments_path = models.CharField(max_length=250, default=settings.S3_FILE_ATTACHMENTS_PATH)
    file_url = models.CharField(max_length=1000, null=True, blank=True)
    file_size = models.BigIntegerField(default=0)
    date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'attachments'
        app_label = 'data'
        
    objects = models.Manager()
    data_ = AttachmentsDataManager()
 