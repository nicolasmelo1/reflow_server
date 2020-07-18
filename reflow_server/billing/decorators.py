from django.urls import resolve
from django.http import JsonResponse

from rest_framework import status

from reflow_server.billing.services.permissions import BillingPermissionService
from reflow_server.authentication.decorators import permission_required

from functools import wraps


def validate_billing(function):
    @wraps(function)
    def validate_billing_wrap(request, *args, **kwargs):
        company_id = kwargs.get('company_id', None)
        url_name = resolve(request.path_info).url_name
        files = request.FILES
        
        billing_permission_service = BillingPermissionService(company_id=company_id, url_name=url_name, files=files)
        if not billing_permission_service.is_valid():
            return JsonResponse({
                'status': 'error'
            }, status=status.HTTP_404_NOT_FOUND)
           
        return function(request, *args, **kwargs)
    
    return validate_billing_wrap