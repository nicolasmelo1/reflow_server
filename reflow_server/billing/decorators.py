from django.http import JsonResponse

from reflow_server.authentication.models import Company
from reflow_server.billing.models import CompanyBilling
from reflow_server.core.permissions import validate_permissions_from_request, PermissionsError
from reflow_server.authentication.decorators import permission_required

from functools import wraps
import json


def validate_billing(function):
    @wraps(function)
    @permission_required
    def validate_billing_wrap(request, *args, **kwargs):
        # validates only companies that are not supercompanies. Supercompanies can be bypassed
        company = Company.objects.filter(id=kwargs.get('company_id', None)).first()
        company_billing = CompanyBilling.objects.filter(company=company).first()
        if company and company_billing and not company_billing.is_supercompany:
            try:
                validate_permissions_from_request(request, 'billing', **kwargs)
            except PermissionsError as pe:
                return JsonResponse({
                    'status': 'error',
                    'reason': pe.detail
                }, status=pe.status)
        return function(request, *args, **kwargs)
    
    return validate_billing_wrap
    