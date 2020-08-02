from django.urls import resolve
from django.http import JsonResponse

from rest_framework import status

from reflow_server.authentication.services import permissions
from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.authentication.models import UserExtended

from functools import wraps


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


def permission_required(function):
    """
    Validates all of the permission of a user while validating if the user is logged or not.
    This decorator also automatically decrypts the company_id for you, so you don't have to care about it.
    This decorator is used primarly on view functions. So in order to render a response to a user it first needs
    to check if the user is accessing the data that he has access to.  If the user is not valid in some of these validations, since he
    is logged in, we render a dumb 404 face in the content with menus on top so he can navigate in our website.

    It's important to notice that it is a good practice to use the same url parameters if the data is the same. I mean, if you have
    are recieving a form_id as the parameter of the url, try to write urls like
    
    >>> re_path(r'^depends_on/(?P<form_id>\d+)/$', validate_permissions(APIThemeDependentForms.as_view()), name='manage_theme_dependent_forms_api'),

    instead of

    >>> re_path(r'^depends_on/(?P<id_of_the_form>\d+)/$', validate_permissions(APIThemeDependentForms.as_view()), name='manage_theme_dependent_forms_api'),

    this is because this function use the name form_id to validate, so it defines some small patterns and rules to follow in your code.
    """
    @wraps(function)
    @jwt_required
    def permission_required_wrap(request, *args, **kwargs):
        company_id = kwargs.get('company_id', None)
        user_id = kwargs.get('user_id', None) if kwargs.get('user_id', None) else request.user.id
        form = kwargs.get('form', None)
        form_id = kwargs.get('form_id', None)
        dynamic_form_id = kwargs.get('dynamic_form_id', None)
        section_id = kwargs.get('section_id', None)
        field_id = kwargs.get('field_id', None)
        notification_configuration_id = kwargs.get('notification_configuration_id', None)
        kanban_card_id = kwargs.get('kanban_card_id', None)
        url_name = resolve(request.path_info).url_name

        # generic errors are required so the user don't force to try to uncover his permissions
        if user_id and company_id:
            permission_service = permissions.PermissionService(
                user_id=user_id, company_id=Encrypt.decrypt_pk(company_id), form_name=form, form_id=form_id,
                dynamic_form_id=dynamic_form_id, section_id=section_id, field_id=field_id,
                notification_configuration_id=notification_configuration_id, kanban_card_id=kanban_card_id,
                url_name=url_name
            )
            if not permission_service.is_valid():
                return JsonResponse({
                    'status': 'error',
                    'reason': 'not_permitted'
                }, status=status.HTTP_404_NOT_FOUND)
            else:
                # automatically decrypts the company_id pk for your views
                kwargs['company_id'] = Encrypt.decrypt_pk(company_id)
        else:
            return JsonResponse({
                'status': 'error',
                'reason': 'not_permitted'
            }, status=status.HTTP_404_NOT_FOUND)

        return function(request, *args, **kwargs)
        
    return permission_required_wrap