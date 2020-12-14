from django.db import models


class PDFTemplateConfigurationVariablesPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def delete_pdf_template_configuration_variables_from_pdf_template_id_and_field_ids(self, pdf_template_id, field_ids):
        """
        Deletes the PDFTemplateConfigurationVariables of a pdf_template_id excluding a list of ids from the deletion.

        Args:
            pdf_template_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id
            field_ids (list(int)): A list of reflow_server.pdf_generator.models.Field instances
                                   ids. We use this list to filter them on the deletion. So we will remove
                                   all of the ids that ARE ON THIS LIST

        Returns:
            int: The number of removed PDFTemplateConfigurationVariables instances.
        """
        return self.get_queryset().filter(pdf_template_id=pdf_template_id, field_id__in=field_ids).delete()

    def pdf_template_configuration_variables_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        """
        Returns a queryset of PDFTemplateConfigurationVariables of a pdf_template_configuration_id. We use this so we can
        get the fields of a pdf_template_configuration

        Args:
            pdf_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id

        Returns:
            django.db.models.QuerySet(reflow_server.pdf_generator.models.PDFTemplateConfigurationVariables): A querset of template configuration
            variables. 
        """
        return self.get_queryset().filter(pdf_template_id=pdf_template_configuration_id)

    def field_ids_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        """
        Returns a queryset of Field instances ids from the PDFTemplateConfiguration instance id.

        Args:
            pdf_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration intance id

        Returns:
            django.db.models.QuerySet(int): A queryset of field intances ids
        """
        return self.get_queryset().filter(pdf_template_id=pdf_template_configuration_id).values_list('field_id', flat=True)

    def update_or_create(self, field_id, pdf_template_id, pdf_template_configuration_variable_id=None):
        """
        Updates or creates a PDFTemplateConfigurationVariable instance. If the pdf_template_configuration_variable_id parameter
        is None we will create, otherwise we will update the instance if it existis.

        Args:
            field_id (int): A reflow_server.formulary.models.Field instance id
            pdf_template_id (int): A reflow_server.pdf_generator.models.PDFConfigurationTemplate instance id
            pdf_template_configuration_variable_id (int, optional): A reflow_server.pdf_generator.models.PDFConfigurationTemplateVariables instance id. 
                                                                    Defaults to None.

        Returns:
            reflow_server.pdf_generator.models.PDFConfigurationTemplateVariables: The updated or created instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            id=pdf_template_configuration_variable_id,
            defaults={
                'field_id': field_id,
                'pdf_template_id': pdf_template_id
            }
        )
        return instance