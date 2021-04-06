
from django.db import models


class PDFTemplateConfigurationPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def rich_text_page_id_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        """
        It's important to understand that it's not obligatory to use the RichText to create pdf templates.
        At least for the long run it will not be obligatory. 
        So this function is responsible for retriving the rich_te_idxt_page that a pdf_template_configuration_id 
        is bounded to

        Args:
            pdf_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id

        Returns:
            int: Returns a reflow_server.rich_text.models.TextPage instance id.
        """
        return self.get_queryset().filter(id=pdf_template_configuration_id).values_list('rich_text_page_id', flat=True).first()

    def pdf_template_configurations_by_user_id_company_id_and_form_name_ordered_by_id(self, user_id, company_id, form_name):
        """
        Gets a queryset of PDFTemplateConfiguration instances from a user_id, a company_id and that is bounded
        to a specific form_name. Ordered by id, getting the last to the first.

        Args:
            user_id (int): A reflow_server.authentication.models.UserExtended instance id
            company_id (int): A reflow_server.authentication.models.Company instance id
            form_name (str): The form_name of a formulary. This form_name works like an id for each form. 
                             This is unique for each company.

        Returns:
            django.db.models.QuerySet(reflow_server.pdf_generator.models.PDFTemplateConfiguration): The PDFTemplateConfiguration instances
        """
        return self.pdf_template_configurations_by_company_id_and_form_name_ordered_by_id(company_id, form_name).filter(user_id=user_id).order_by('-id')

    def pdf_template_configurations_by_company_id_and_form_name_ordered_by_id(self, company_id, form_name):
        """
        Gets a queryset of PDFTemplateConfiguration instances by the company_id and the form_name. Ordered by id, getting the last to the first.

        Args:
            company_id (int): A reflow_server.authentication.models.Company instance id
            form_name (str): The form_name of a formulary. This form_name works like an id for each form. 
                             This is unique for each company. 

        Returns:
            django.db.models.QuerySet(reflow_server.pdf_generator.models.PDFTemplateConfiguration): The PDFTemplateConfiguration instances
        """
        return self.get_queryset().filter(company_id=company_id, form__form_name=form_name).order_by('-id')

    def pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(self, user_id, company_id, form_name, pdf_template_configuration_id):
        """
        Get a single PDFTemplateConfiguration by its user, its company the form_name and also its id. Why would you need all of this you might ask.
        And for that the answer is that we need to make sure the user is only retrieving the data that he absolutely sure have access to.

        Args:
            user_id (int): A reflow_server.authentication.models.UserExtended instance id
            company_id (int): A reflow_server.authentication.models.Company instance id
            form_name (str): The form_name of a formulary. This form_name works like an id for each form. 
                             This is unique for each company.
            pdf_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id

        Returns:
            reflow_server.pdf_generator.models.PDFTemplateConfiguration: A single PDFTemplateConfiguration instance filtered by the user,
                                                                         the form_name, company_id and also the pdf_template_configuration_id
        """
        return self.pdf_template_configurations_by_user_id_company_id_and_form_name_ordered_by_id(user_id, company_id, form_name).filter(id=pdf_template_configuration_id).first()

    def remove_pdf_template_configuration_by_template_configuration_id_company_id_and_user_id(self, pdf_template_configuration_id, company_id, user_id):
        """
        Deletes a single PDFTemplate instance by it's id, the company_id and the user that created.

        Args:
            pdf_template_configuration_id (int): The PDFTemplateConfiguration instance id to be removed
            company_id (int): A reflow_server.authentication.models.Company instance id
            user_id (int): A reflow_server.authentication.models.UserExtended instance id

        Returns:
            int: The number of removed instances, usually it will be just one.
        """
        return self.get_queryset().filter(id=pdf_template_configuration_id, company_id=company_id, user_id=user_id).delete()

    def update_or_create_pdf_template_configuration(self, name, company_id, user_id, form_id, pdf_template_configuration_id=None, rich_text_page_id=None):
        """
        Updates or creates a PDFTemplateConfiguration. If the pdf_template_configuration_id parameter is None we 
        will create a new template, otherwise we will update (if the id exists in the database.)

        Args:
            name (str): The name of the template. So the user can diferentiate between templates
            company_id (int): A reflow_server.authentication.models.Company instance id
            user_id (int): A reflow_server.authentication.models.UserExtended instance id
            form_id (int): A reflow_server.formulary.models.Formulary instance id. Every template is bounded
                           to a formulary.
            pdf_template_configuration_id (int, optional): The id of the template you want to edit. Defaults to None.

        Returns:
            reflow_server.pdf_generator.models.PDFTemplateConfiguration: The created or updated instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            id=pdf_template_configuration_id, 
            defaults={
                'company_id': company_id,
                'user_id': user_id,
                'form_id': form_id,
                'name': name,
                'rich_text_page_id': rich_text_page_id
            }
        )
        
        return instance