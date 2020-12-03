
from django.db import models


class PDFTemplateConfigurationPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def pdf_template_configurations_by_user_id_company_id_and_form_name(self, user_id, company_id, form_name):
        return self.get_queryset().filter(user_id=user_id, company_id=company_id, form__form_name=form_name)

    def pdf_template_configuration_by_user_id_company_id_and_form_name_and_pdf_template_configuration_id(self, user_id, company_id, form_name, pdf_template_configuration_id):
        return self.pdf_template_configurations_by_user_id_company_id_and_form_name(user_id, company_id, form_name).filter(id=pdf_template_configuration_id).first()

    def update_or_create_pdf_template_configuration(self, name, company_id, user_id, form_id, pdf_template_configuration_id=None):
        instance, __ = self.get_queryset().update_or_create(
            id=pdf_template_configuration_id, 
            defaults={
                'company_id': company_id,
                'user_id': user_id,
                'form_id': form_id,
                'name': name
            }
        )
        
        return instance