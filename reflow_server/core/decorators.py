from django.conf import settings
from django.http import JsonResponse

from reflow_server.core.services.external import ExternalService
from reflow_server.authentication.decorators import jwt_required, permission_required
from reflow_server.billing.decorators import validate_billing
from functools import wraps
import requests


def authorize_external_response(function):
    """
    Some urls needs to be protected because sometimes we want to send data from many users or about a 
    single user between internal apps.
    For those cases we protect the urls with this decorator. This decorator is responsible for validating 
    if the request has an HTTP_AUTHORIZATION header disposed by the AUTH_BEARER app. 
    We then use this header and checks in the AUTH_BEARER app. If this JWT is invalid or non existent 
    we respond that this request is invalid.

    It's important to notice that this is extremely important only when the app is on server environment, 
    so staging and production; for development no such thing is necessary.
    """
    @wraps(function)
    def authorize_external_response_wrap(request, *args, **kwargs):
        if ExternalService.is_response_authorized(request):
            return function(request, *args, **kwargs)
        else:
            return JsonResponse({'msg': 'request not authorized'}, status=403)
            
    return authorize_external_response_wrap