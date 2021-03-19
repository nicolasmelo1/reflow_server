from rest_framework import status

from reflow_server.pdf_generator.services.permissions import PDFGeneratorPermissionsService
from reflow_server.core.permissions import PermissionsError


class PDFGeneratorBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None):
        self.company_id = company_id

    def __call__(self, request):
        from reflow_server.pdf_generator.services.routes import pdf_generator_generate_url_name 
        
        if request.url_name in pdf_generator_generate_url_name and \
            not PDFGeneratorPermissionsService.can_generate_pdf(self.company_id):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
