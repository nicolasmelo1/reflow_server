from reflow_server.pdf_generator.models import PDFGenerated
from reflow_server.billing.models import CurrentCompanyCharge


class PDFGeneratorPermissionsService:
    @staticmethod
    def can_generate_pdf(company_id):
        """
        Checks if the user can download a pdf template. We limit the number of downloads the user can make
        so he pays more for the funcionality.

        Args:
            company_id (int): A reflow_server.authentication.models.Company instance id

        Returns:
            bool: Returns true or false. True if the user can download a PDF, False if not.
        """
        total_pdfs_of_company = PDFGenerated.pdf_generator_.total_generated_pdfs_by_company(company_id=company_id)
        permitted_total_pdfs_of_company = CurrentCompanyCharge.objects.filter(company_id=company_id, individual_charge_value_type__name='per_pdf_download')\
            .order_by('-quantity')\
            .values_list('quantity', flat=True).first()
        
        if total_pdfs_of_company >= permitted_total_pdfs_of_company:
            return False
        return True