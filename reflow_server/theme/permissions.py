from rest_framework import status

from reflow_server.theme.services.permissions import ThemePermissionService
from reflow_server.core.permissions import PermissionsError


class ThemeDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, theme_id=None):
        self.theme_id = theme_id
        self.company_id = company_id

    def __call__(self, request):
        if self.theme_id and not ThemePermissionService.is_valid(request.request.user, self.company_id, self.theme_id):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)


class ThemeBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, selected_theme_id=None):
        self.theme_id = selected_theme_id
        self.company_id = company_id

    def __call__(self, request):
        if request.url_name == 'theme_select' and request.method == 'POST':
            if not ThemePermissionService.can_add_theme_based_on_number_of_pages_permission(self.company_id, self.theme_id):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
