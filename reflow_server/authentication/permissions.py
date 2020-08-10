from rest_framework import status

from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.services.permissions import AuthenticationPermissionsService
from reflow_server.core.permissions import PermissionsError


class AuthenticationDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, user_id=None):
        self.company_id = company_id
        self.user_id = user_id
    
    def __call__(self, request):
        self.user_id = self.user_id if self.user_id else request.request.user.id 
        
        user = UserExtended.objects.filter(id=self.user_id).first()
        company = Company.objects.filter(id=self.company_id).first()

        if not all([
            AuthenticationPermissionsService.is_valid_compay(company), 
            AuthenticationPermissionsService.is_valid_user_company(company, user), 
            AuthenticationPermissionsService.is_valid_admin_only_path(user, request.url_name)
        ]):
            raise PermissionsError(detail='not_permitted', status_code=status.HTTP_404_NOT_FOUND)
