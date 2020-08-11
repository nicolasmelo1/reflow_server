from rest_framework import status

from reflow_server.billing.services.permissions import BillingPermissionsService
from reflow_server.core.permissions import PermissionsError


class BillingBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None):
        self.company_id = company_id

    def __call__(self, request):
        if self.company_id and not BillingPermissionsService.is_valid_free_trial(self.company_id):
            raise PermissionsError(detail='free_trial_ended', status=status.HTTP_403_FORBIDDEN)
