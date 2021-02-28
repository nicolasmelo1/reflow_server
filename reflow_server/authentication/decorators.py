from django.http import JsonResponse

from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.permissions import validate_permissions_from_request, PermissionsError, PublicPermissionIsValidError
from reflow_server.authentication.utils.jwt_auth import JWT

from functools import wraps

# ------------------------------------------------------------------------------------------
def jwt_required(function):
    """
    Decorator used for validating if a user is logged in and authenticated or not.
    If you are using the `.permission_required()` decorator, you don't need this function
    """
    @wraps(function)
    def jwt_required_wrap(request, *args, **kwargs):
        jwt = JWT()
        jwt.extract_jwt_from_request(request)
        if jwt.is_valid():
            return function(request, *args, **kwargs)
        elif jwt.error in ['jwt_not_defined', 'unknown_error']:
            return JsonResponse({
                'status': 'error',
                'reason': 'login_required'
            }, status=status.HTTP_403_FORBIDDEN)
        else:
            return JsonResponse({
                'status': 'error',
                'reason': jwt.error
            }, status=status.HTTP_403_FORBIDDEN)

    return jwt_required_wrap
# ------------------------------------------------------------------------------------------
def get_company_id_as_int(function):
    """
    This decorator automatically decrypts the company_id for you, so you don't have to care about it in you views.
    """
    @wraps(function)
    def get_company_id_as_int_wrap(request, *args, **kwargs):
        if kwargs.get('company_id', None):
            kwargs['company_id'] = Encrypt.decrypt_pk(kwargs.get('company_id', None)) if kwargs.get('company_id', None) else None
        return function(request, *args, **kwargs)

    return get_company_id_as_int_wrap
# ------------------------------------------------------------------------------------------
def logged_in_user_permission_required(function):
    @wraps(function)
    @jwt_required
    @get_company_id_as_int
    def logged_in_user_permission_required_wrap(request, *args, **kwargs):
        try:
            validate_permissions_from_request(request, 'default', **kwargs)
        except PermissionsError as pe:
            return JsonResponse({
                'status': 'error',
                'reason': pe.detail
            }, status=pe.status)

        return function(request, *args, **kwargs)
    
    return logged_in_user_permission_required_wrap
# ------------------------------------------------------------------------------------------
def public_access_permissions(function):
    @wraps(function)
    @get_company_id_as_int
    def public_access_permissions_wrap(request, *args, **kwargs):
        try:
            validate_permissions_from_request(request, 'public', **kwargs)
        except PermissionsError as pe:
            pass
        except PublicPermissionIsValidError as ppiv:
            return function(request, *args, **kwargs)
        return JsonResponse({
            'status': 'error',
            'reason': 'api_is_not_public'
        }, status=400)
    
    return public_access_permissions_wrap
# ------------------------------------------------------------------------------------------
def permission_required(function):
    """
    Validates all of the permission of a user while validating if the user is logged or not.
    This decorator is used primarly on view functions. So in order to render a response to a user it first needs
    to check if the user is accessing the data that he has access to.  If the user is not valid in some of these validations, since he
    is logged in, we render a dumb 404 face in the content with menus on top so he can navigate in our website.

    This decorator uses `validate_permissions_from_request` function, so you might want to read it before trying to understand this.
    """
    @wraps(function)
    def permission_required_wrap(request, *args, **kwargs):
        if getattr(request, 'is_public', False):
            decorated = public_access_permissions(function)
            return decorated(request, *args, **kwargs)
        else:
            decorated = logged_in_user_permission_required(function)
            return decorated(request, *args, **kwargs)
        
    return permission_required_wrap