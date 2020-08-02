from django.urls import resolve
from django.http import JsonResponse

from rest_framework import status

from reflow_server.billing.services.permissions import BillingPermissionService
from reflow_server.authentication.decorators import permission_required

from functools import wraps
import json

def validate_billing(function):
    def get_json_data_from_request_body(body):
        try:
            return json.loads(body.decode('utf-8'))
        except:
            return {}


    @wraps(function)
    @permission_required
    def validate_billing_wrap(request, *args, **kwargs):
        company_id = kwargs.get('company_id', None)
        user_id = kwargs.get('user_id', None) if kwargs.get('user_id', None) else request.user.id
        form = kwargs.get('form', None)
        dashboard_configuration_id = kwargs.get('dashboard_configuration_id', None)
        url_name = resolve(request.path_info).url_name
        files = request.FILES
        for_company = get_json_data_from_request_body(request.body).get('for_company', None)
        billing_permission_service = BillingPermissionService(company_id=company_id, user_id=user_id, for_company=for_company,  
                                                              request_method=request.method, form_name=form,
                                                              dashboard_configuration_id=dashboard_configuration_id, 
                                                              url_name=url_name, files=files)
        if not billing_permission_service.is_valid_free_trial():
            return JsonResponse({
                'status': 'error',
                'reason': 'free_trial_ended'
            }, status=status.HTTP_403_FORBIDDEN)
        if not billing_permission_service.is_valid():
            return JsonResponse({
                'status': 'error',
                'reason': 'invalid_billing'
            }, status=status.HTTP_403_FORBIDDEN)
           
        return function(request, *args, **kwargs)
    
    return validate_billing_wrap