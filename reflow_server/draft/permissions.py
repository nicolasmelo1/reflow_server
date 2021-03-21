from rest_framework import status

from reflow_server.core.permissions import PermissionsError
from reflow_server.draft.services.permissions import DraftPermissionService


class DraftBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None):
        self.company_id = company_id

    def __call__(self, request):
        from reflow_server.draft.services.routes import draft_url_names
        
        if request.url_name in draft_url_names and request.method in ['PUT', 'POST']:
            if not DraftPermissionService.validate_file_upload(self.company_id, request.files):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
            
