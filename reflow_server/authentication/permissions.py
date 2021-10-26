from rest_framework import status

from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.services.permissions import AuthenticationPermissionsService
from reflow_server.core.permissions import PermissionsError, PublicPermissionIsValidError


class AuthenticationDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, user_id=None):
        self.company_id = company_id
        self.user_id = user_id
    
    def __call__(self, request):
        self.user_id = request.request.user.id if request.request.user.is_authenticated else self.user_id
        
        user = UserExtended.authentication_.user_by_user_id(self.user_id)
        if not AuthenticationPermissionsService.is_valid_admin_only_path(user, request.url_name):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)

        if self.company_id:
            company = Company.authentication_.company_by_company_id(self.company_id)

            if not AuthenticationPermissionsService.is_valid_compay(company) or not AuthenticationPermissionsService.is_valid_user_company(company, user):
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)


class AuthenticationPublicPermission:
    """
    IMPORTANT: This should come as late as possible in the permissions list because we validate if the url is a public url
    if it comes too early we will skip the rest of the permissions.
    
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, user_id=None):
        self.company_id = company_id
        self.user_id = user_id
    
    def __call__(self, request):
        self.user_id = request.request.user.id if request.request.user.is_authenticated else self.user_id
        
        user = UserExtended.authentication_.user_by_user_id(self.user_id)

        if self.company_id:
            company = Company.authentication_.company_by_company_id(self.company_id)
            if not AuthenticationPermissionsService.is_valid_compay(company) or not AuthenticationPermissionsService.is_valid_user_company(company, user):
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)

        if not AuthenticationPermissionsService.is_valid_public_path(request.url_name):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)
        else:
            raise PublicPermissionIsValidError(detail='valid')
