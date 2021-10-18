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
    """
    This is used to validating all of the permissions of the user. Does the user have access to it, or not. 
    By default the users have permission FOR EVERYTHING you need to block what he can and what he can't acess
    creating custom permission classes inside of the apps.

    Permissions are not default to django, we've created it the same way as Django Rest Framework adds the `serializers.py` files
    we add the `permissions.py` files. To understand how permissions work read 
    `reflow_server.core.permissions.validate_permissions_from_request` to understand how to create permissions and 
    to validate if the users have an access or not.
    """
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
    """
    THIS IS HIGHLY SENSITIVE, AND CAN BRING LEGAL ISSUES IF DONE WRONG, SO BE AWARE OF THIS WHEN MAKING CHANGES

    This validates if an Unauthenticated user can access some content or not. By default, THE USER CANNOT ACCESS ANYTHING UNAUTHENTICATED.
    So you need to throw an error in your permission class, allowing the user to access some content. I know that this might seem counter
    intuitive, but we need to make it this way. Be aware that this can expose sensitive information about the user to the public,
    so make a lot of tests to guarantee you are not exposing any sensitive information of the user. And that also you are NOT allowing the public
    to make any changes to the user data WITHOUT the user consent.

    Permissions are not default to django, we've created it the same way as Django Rest Framework adds the `serializers.py` files
    we add the `permissions.py` files. To understand how permissions work read 
    `reflow_server.core.permissions.validate_permissions_from_request` to understand how to create permissions and 
    to validate if the users have an access or not.
    """
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
        }, status=status.HTTP_403_FORBIDDEN)
    
    return public_access_permissions_wrap
# ------------------------------------------------------------------------------------------
def permission_required(function):
    """
    Simple middleware that validates the permissions of the users.
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
# ------------------------------------------------------------------------------------------
def api_token_required(function):
    from reflow_server.billing.decorators import validate_billing

    @wraps(function)
    @get_company_id_as_int
    def api_token_required_wrap(request, *args, **kwargs):
        return function(request, *args, **kwargs)
    
    return api_token_required_wrap
