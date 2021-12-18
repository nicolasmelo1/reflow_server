from rest_framework import status

from reflow_server.dashboard.services.permissions import DashboardPermissionsService
from reflow_server.core.permissions import PermissionsError


class DashboardDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, form=None, dashboard_configuration_id=None):
        self.company_id = company_id
        self.form = form
        self.dashboard_configuration_id = dashboard_configuration_id

    def __call__(self, request):
        if self.company_id and self.form and self.dashboard_configuration_id and \
            not DashboardPermissionsService.is_valid(self.company_id, self.form, self.dashboard_configuration_id):
                raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)


class ChartsBillingPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, company_id=None, form=None, dashboard_configuration_id=None):
        self.company_id = company_id
        self.form = form
        self.dashboard_configuration_id = dashboard_configuration_id

    def __call__(self, request):
        from reflow_server.dashboard.services.routes import dashboard_settings_url_names

        if request.url_name in dashboard_settings_url_names and request.method == 'POST':

            for_company = request.data.get('for_company', False) if type(request.data) == dict else False

            if not DashboardPermissionsService.is_valid_billing_charts(
                    self.company_id, request.request.user.id, self.form, for_company, self.dashboard_configuration_id
                ):
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
