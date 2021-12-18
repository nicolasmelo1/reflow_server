from reflow_server.pdf_generator.models import PDFGenerated
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.services import BillingService


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
        total_pdfs_of_company = PDFGenerated.pdf_generator_.total_generated_pdfs_by_company_in_current_month(company_id=company_id)
        permitted_total_pdfs_of_company = CurrentCompanyCharge.pdf_generator_.quantity_of_per_charts_permission_for_company_id(company_id=company_id)
        
        if total_pdfs_of_company >= permitted_total_pdfs_of_company:
            return False
        return True