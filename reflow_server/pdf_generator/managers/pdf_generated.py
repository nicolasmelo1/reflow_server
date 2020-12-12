from django.db import models
from django.utils import timezone

class PDFGeneratedPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def total_generated_pdfs_by_company_in_current_month(self, company_id):
        """
        Retrives the total of generated pdfs of the company. This way we can prevent the user
        from generating new pdfs so that he needs to pay more.

        Args:
            company_id (int): A reflow_server.authentication.models.Company instance id

        Returns:
            int: The number of created instances in the current month
        """
        month = timezone.now().month
        return self.get_queryset().filter(company_id=company_id, created_at__month=month).count()
        
    def create(self, company_id, user_id, pdf_template_configuration_id):
        return self.get_queryset().create(
            company_id=company_id,
            user_id=user_id,
            pdf_template_id=pdf_template_configuration_id
        )
