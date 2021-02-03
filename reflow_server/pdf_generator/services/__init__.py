from django.db import transaction
from django.db.utils import IntegrityError

from reflow_server.pdf_generator.models import PDFTemplateConfiguration, \
    PDFTemplateConfigurationVariables
from reflow_server.pdf_generator.services.data import PDFVariablesData
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.formulary.models import Form, Field
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.rich_text.models import TextPage
from reflow_server.rich_text.services import RichTextService


class PDFGeneratorService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.pdf_generator_.formulary_by_company_id_and_form_name(company_id, form_name)

    @property
    def form_options_to_use_on_template(self):
        """
        This function returns the form_options the user can use in the template text.
        Right now it only goes ONE LEVEL deep. So if you have a the 'Sales Pipeline' formulary and this formulary is connected through 'form'
        field with 'Client' we get the `Sales Pipeline` fields and `Client` fields. If `Sales Pipeline` is connected to any other
        formulary we also get this other formulary fields.

        ONE LEVEL DEEP means that, if `Client` is connected to any other formulary we will NOT get this other formulary field options. We do this
        as you might think to prevent recursion from happening. If we hadn't set a break to our platform it would explode. (not literally)

        Returns:
            tuple(
                list(reflow_server.formulary.models.Form),
                {
                    reflow_server.formulary.models.Form.id: [reflow_server.formulary.models.Field]
                }
            ): List of Form instances so we can use it in our serializers.
        """
        form_from_connected_field_helper = {}
        form_options = [self.form]
        formulary_service = FormularyService(self.user_id, self.company_id)
        form_ids_the_user_has_access_to = formulary_service.formulary_ids_the_user_has_access_to
        form_type_fields = Field.pdf_generator_.form_fields_by_main_form_id_and_company_id(self.form.id, self.company_id)
        for field in form_type_fields:
            if field.form_field_as_option.form.depends_on_id in form_ids_the_user_has_access_to:
                form_options.append(field.form_field_as_option.form.depends_on)
                # sometimes a field can be bounded to the same form, this way we can differentiate between each of them.
                form_from_connected_field_helper[field.form_field_as_option.form.depends_on_id] = \
                    form_from_connected_field_helper.get(field.form_field_as_option.form.depends_on_id, []) + [field]

        return form_options, form_from_connected_field_helper

    @transaction.atomic
    def remove_pdf_template(self, pdf_template_id):
        """
        Removes a PDF template. It's important to notice that when we remove a PDFTemplate we also need to remove the RichTextPage it is bound to
        that's what we do here.

        Args:
            pdf_template_id (int): The id of the pdf_template_configuration you want to remove.

        Returns:
            int: The number of PDFTemplateConfiguration instances removed, usually just one.
        """
        rich_text_page_id = PDFTemplateConfiguration.pdf_generator_.rich_text_page_id_by_pdf_template_configuration_id(pdf_template_id)

        if rich_text_page_id:
            rich_text_service = RichTextService(self.company_id, self.company_id)
            rich_text_service.remove_page(rich_text_page_id)

        return PDFTemplateConfiguration.pdf_generator_.remove_pdf_template_configuration_by_template_configuration_id_company_id_and_user_id(
            pdf_template_id, self.company_id, self.user_id
        )

    @transaction.atomic
    def save_pdf_template(self, name, pdf_variables_data, page_data=None, pdf_template_id=None):
        """
        This save can be quite tricky but it's not that difficult to grasp. 
        - First we create the TextPage if the page_data parameter is defined and not None.
        - Then we create the PDFTemplateConfiguration instance that we bound with the page if needed.
        - Then we save all of the variables (we save them so we can increase the performance when 
        retrieving the data needed for the reader, also the pdf functionality can have almost full control
        of the data flow without needing and depending much on the RichText)
        - After inserting the variables we remove the unused ones.

        (RichText is not obligatory because we want to offer some integrations so the users will not be locked on creating
        PDFTemplates using ONLY our RichText)

        Args:
            name (str): The name of the this PDFTemplate
            pdf_variables_data (reflow_server.pdf_generator.services.data.PDFVariablesData): This is used so we do not become 
            dependent on serializers, we can change the serializers the way we want.
            page_data (reflow_server.rich_text.services.data.PageData, optional): The PageData object, this object holds 
            everything about the RichText, it's blocks and each contents of the block. You can read it in the class constructor. 
            Defaults to None.
            pdf_template_id (int, optional): The template configuration id, set this to None if you are creating a new template,
            if an int is recieved then we will update the template. Defaults to None.

        Returns:
            reflow_server.pdf_generator.models.PDFTemplateConfiguration: the newly created PDFTemplateConfiguration instance.
        """
        rich_text_page_id = None
        if page_data:
            rich_text_service = RichTextService(self.company_id, self.user_id)
            rich_text_page_instance = rich_text_service.save_rich_text(page_data)
            rich_text_page_id = rich_text_page_instance.id
            
        pdf_template_configuration_instance = PDFTemplateConfiguration.pdf_generator_.update_or_create_pdf_template_configuration(
            name, self.company_id, self.user_id, self.form.id, pdf_template_id, rich_text_page_id
        )

        # adds the variables and deletes the removed variables.
        field_ids_to_add, field_ids_to_exclude = pdf_variables_data.variables
        PDFTemplateConfigurationVariables.pdf_generator_.delete_pdf_template_configuration_variables_from_pdf_template_id_and_field_ids(
            pdf_template_configuration_instance.id, field_ids_to_exclude
        )
        for field_id in field_ids_to_add: 
            try:
                PDFTemplateConfigurationVariables.pdf_generator_.update_or_create(
                    field_id, pdf_template_configuration_instance.id, None
                )
            except IntegrityError as ie:
                pass
        return pdf_template_configuration_instance

    def field_values_to_use_on_template(self, pdf_template_configuration_id, form_data_id):
        """
        I don't like it either, if you've got a better way to do it, please do it.

        Here we actually need to do many turns in order to get the connect fields. First we get the variables of the template.
        - Then we check if the form of the field of this variable is the SAME as the form_id of the form of the template.
        - If it is not the same we append to a list of form_ids
        - Then we get the form_values that could be either connected to one of those form_ids through form_field_as_option of the field or 
        is directly linked with the form_data_id
        - This gives us a queryset of form_values, some of those are not what we actually want but instead connection form_values
        - We use this connection data to then get the data that we actually want.
        - Last but not least we create a new list, but now filtering the data that we actually want.

        Args:
            pdf_template_configuration_id (int): The template that you are using to retrieve the data.
            form_data_id (int): The DynamicForm id that you want to get data from.

        Returns:
            tuple(
                list(reflow_server.data.models.FormValue),
                {
                    reflow_server.data.models.FormValue.id: list(reflow_server.formulary.models.Field)
                }
            ): The FormValues of the connected forms and the main form.
        """
        form_values_to_use = []
        field_ids = []
        forms_that_is_connected_to_form = []
        form_value_from_connected_field_helper = {}
        pdf_template_configuration_variables = PDFTemplateConfigurationVariables.pdf_generator_.pdf_template_configuration_variables_by_pdf_template_configuration_id(pdf_template_configuration_id)
        for pdf_template_configuration_variable in pdf_template_configuration_variables:
            if pdf_template_configuration_variable.field.form.depends_on_id != self.form.id and \
                pdf_template_configuration_variable.field.form.depends_on_id not in forms_that_is_connected_to_form:
                    forms_that_is_connected_to_form.append(pdf_template_configuration_variable.field.form.depends_on_id)
            field_ids.append(pdf_template_configuration_variable.field_id)
    
        form_values = FormValue.pdf_generator_.form_values_by_field_ids_and_form_data_id_and_forms_connected_to(field_ids=field_ids, form_data_id=form_data_id, forms_connected_to=forms_that_is_connected_to_form)
        form_values_to_use = form_values_to_use + list(form_values)
        print(form_values)
        for form_value in form_values:
            # if the form_value is a connection field get the values of the connected formulary/
            if form_value.field_type.type == 'form':
                # if recieves a section needs to get the main_form_id so we get all of the fields
                main_form_data_id = DynamicForm.pdf_generator_.main_formulary_data_id_by_section_data_id(int(form_value.value))
                connected_form_values = FormValue.pdf_generator_.form_values_by_field_ids_and_form_data_id_and_forms_connected_to(
                    field_ids=field_ids, 
                    form_data_id=main_form_data_id if main_form_data_id else int(form_value.value)
                )
                form_values_to_use = form_values_to_use + list(connected_form_values)
                for connected_form_value in connected_form_values:
                    form_value_from_connected_field_helper[connected_form_value.id] = form_value_from_connected_field_helper.get(connected_form_value.id, []) + [form_value.field] 
            
        form_values = []
        for form_value_to_use in form_values_to_use:
            if form_value_to_use.field.id in field_ids:
                form_values.append(form_value_to_use)

        return form_values, form_value_from_connected_field_helper