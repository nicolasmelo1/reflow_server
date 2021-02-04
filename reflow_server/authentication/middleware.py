from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.http.response import JsonResponse

from reflow_server.authentication.models import UserExtended
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.core.utils.rate_limiting import RateLimiting

@database_sync_to_async
def get_user(user_id):
    user = UserExtended.authentication_.user_by_user_id(user_id)
    if user:
        return user
    else:
        return AnonymousUser()


# HTTP Auth JWT middleware
class AuthJWTMiddleware:
    """
    Custom Django middleware responsible for authenticating the user in request.user.
    It's important to understand that we handle authentication on the Django side, using custom middleware,
    not on DRF side. DRF can be quite complicated and create more code than neeeded. Following some default 
    django guidelines is a lot easier.

    This AUTHENTICATE, and DOES NOT AUTHORIZATE. It means that with this we can append the user to the request.
    We do not block him here from going further in the request.
    The AUTHORIZATION is made through custom decorators using permissions. Check reflow_server.core.permissions
    for further explanation on permissions.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
        rate_limiting = RateLimiting(request)

        if rate_limiting.is_rate_limited():
            return JsonResponse({'status': 'error', 'reason': 'rate_limited'})

        jwt = JWT()
        jwt.extract_jwt_from_request(request)
        if jwt.is_valid():
            payload = jwt.data
            user = UserExtended.authentication_.user_by_user_id(payload['id'])
            if user:
                request.user = request.user if type(request.user) == UserExtended else user
        else:
            request.user = AnonymousUser()

        response = self.get_response(request)
        
        rate_limiting.clean()
        return response

"""
class AuthWebsocketJWTMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope, receive, send):
        return AuthWebsocketJWTMiddlewareInstance(scope, self)
"""

class AuthWebsocketJWTMiddleware(BaseMiddleware):
    """
    Okay, so this middleware is not straight forward, and have some undocummented
    really new features because of django 3.0.

    Refer to this part of the documentation: https://docs.djangoproject.com/en/3.0/topics/async/
    There it is explained that Django 3 will raise such exception if you try to use the ORM from within an async context (which seems to be the case).

    As Django Channels documentation explains solution would be to use sync_to_async as follows:
    https://channels.readthedocs.io/en/latest/topics/databases.html#database-sync-to-async

    You might want to read this stack overflow question to see why i did this way https://stackoverflow.com/a/59653335/13158385
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        user = AnonymousUser()
        jwt = JWT()
        jwt.extract_jwt_from_scope(scope)
        if jwt.is_valid():
            payload = jwt.data
            user = await get_user(payload['id'])
        return await self.inner(dict(scope, user=user), receive, send)