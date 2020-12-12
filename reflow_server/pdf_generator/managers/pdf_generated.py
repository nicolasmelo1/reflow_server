from django.db import models


class PDFGeneratedPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def total_generated_pdfs_by_company(self, company_id):
        return self.get_queryset().filter(company_id=company_id).count()
        
    def create(self, company_id, user_id, pdf_template_configuration_id):
        return self.get_queryset().create(
            company_id=company_id,
            user_id=user_id,
            pdf_template_id=pdf_template_configuration_id
        )
