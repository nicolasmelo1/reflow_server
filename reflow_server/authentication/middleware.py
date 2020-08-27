from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async

from reflow_server.authentication.models import UserExtended
from reflow_server.authentication.utils.jwt_auth import JWT


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
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
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
        return response


class AuthWebsocketJWTMiddleware:
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

    def __call__(self, scope):
        return AuthWebsocketJWTMiddlewareInstance(scope, self)


class AuthWebsocketJWTMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        user = AnonymousUser()
        jwt = JWT()
        jwt.extract_jwt_from_scope(self.scope)
        if jwt.is_valid():
            payload = jwt.data
            user = await get_user(payload['id'])
        inner = self.inner(dict(self.scope, user=user))
        return await inner(receive, send) 
