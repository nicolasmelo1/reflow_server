from django.contrib.auth.models import AnonymousUser

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from reflow_server.authentication.models import UserExtended, PublicAccess
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.authentication.utils import is_valid_uuid


############################################################################################
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
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
############################################################################################
# HTTP AUTH public middleware
class AuthPublicMiddleware:
    """
    THIS IS HIGHLY SENSITIVE, AND CAN BRING LEGAL ISSUES IF DONE WRONG, SO BE AWARE OF THIS WHEN MAKING CHANGES

    This is where things can get a little shady.
    This custom Middleware is responsible for validating and appending if the request you are making is public.
    WHAT?

    So what happens is: we have many urls in this application, one is for getting the data to build the formulary, another is for 
    retrieving the data to build the kanban and so on. What if the user wants to share a kanban card, or a formulary with another people,
    but these people are not logged users from reflow?

    What most people would think of is: Okay, so let's create some public urls that doesn't require login. And this is a valid approach but 
    it makes us need to write the same logic more times, not only on the backend, but also on the front-end.

    The Solution:
    > So, to make everything simpler, i decided to create a unique public_access_key for each user in our platform, this public_access_key
    is a simple uuid. Then we create tables in each app to check what data can be public and what data CAN'T be public.
    What this middleware does is check if the request has a `public_key` query param. If it has than our only job is to get the user bounded to
    this `public_key` and append to the request and also append to the request the `is_public` param, signaling our views and middleware that
    this request is coming from an Unauthenticated user.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    # ------------------------------------------------------------------------------------------
    def __call__(self, request): 
        request.is_public = False
        if 'public_key' in request.GET:
            if is_valid_uuid(request.GET.get('public_key')):
                request.is_public = True
                public_access = PublicAccess.objects.filter(public_key=request.GET.get('public_key')).first()
                request.user = public_access.user
        response = self.get_response(request)
        return response
    # ------------------------------------------------------------------------------------------
# CHANNELS MIDDLEWARE BELOW 
############################################################################################
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
    # ------------------------------------------------------------------------------------------
    async def __call__(self, scope, receive, send):
        user = AnonymousUser()
        jwt = JWT()
        jwt.extract_jwt_from_scope(scope)
        if jwt.is_valid():
            payload = jwt.data
            user = await self.get_user(payload['id'])
        return await self.inner(dict(scope, user=user), receive, send)
    # ------------------------------------------------------------------------------------------
    @database_sync_to_async
    def get_user(self, user_id):
        user = UserExtended.authentication_.user_by_user_id(user_id)
        if user:
            return user
        else:
            return AnonymousUser()
############################################################################################
class AuthWebsocketPublicMiddleware(BaseMiddleware):
    """
    Similar to `AuthPublicMiddleware` but for Websockets. This also DOES NOT ADD THE USER TO THE SCOPE.
    On `AuthPublicMiddleware` we add the user to the request because we can have some issues using that. 
    Here WE DO NOT add him to the scope. If we added we would be able to connect to UserConsumer, with a public_key
    that would be WRONG so users would be able to see sensitive information in the websockets. (it's important
    to understand that this happens ONLY if we ad the middleware on the URLRouter lever AND NOT on the Consumer
    level, as it is today.) 

    THIS IS HIGHLY SENSITIVE, AND CAN BRING LEGAL ISSUES IF DONE WRONG, SO BE AWARE OF THIS WHEN MAKING CHANGES
    """
    def __init__(self, inner):
        self.inner = inner
    # ------------------------------------------------------------------------------------------
    async def __call__(self, scope, receive, send):
        if 'query_string' in scope and 'public_key=' in str(scope['query_string']):
            public_access_key = scope['query_string'].decode('utf-8').replace('public_key=', '')
            if await self.does_public_access_key_exists(public_access_key):
                return await self.inner(dict(scope, is_public=True), receive, send)
        return await self.inner(dict(scope, is_public=False), receive, send)
    # ------------------------------------------------------------------------------------------
    @database_sync_to_async
    def does_public_access_key_exists(self, public_access_key):
        return PublicAccess.objects.filter(public_key=public_access_key).exists()
    # ------------------------------------------------------------------------------------------
