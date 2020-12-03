from django.db import models


class PDFTemplateConfigurationVariablesPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def delete_pdf_template_configuration_variables_from_pdf_template_id_excluding_variable_ids(self, pdf_template_id, pdf_template_configuration_variable_ids):
        return self.get_queryset().filter(pdf_template_id=pdf_template_id).exclude(id__in=pdf_template_configuration_variable_ids).delete()

    def update_or_create(self, field_id, pdf_template_id, pdf_template_configuration_variable_id=None):
        instance, __ = self.get_queryset().update_or_create(
            id=pdf_template_configuration_variable_id,
            defaults={
                'field_id': field_id,
                'pdf_template_id': pdf_template_id
            }
        )
        return instance