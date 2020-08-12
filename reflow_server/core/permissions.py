from django.conf import settings
from django.urls import resolve

import inspect
import json


class PermissionsError(Exception):
    def __init__(self, detail, status):
        """
        This class is used for exception handling. Inside of permission classes.

        Args:
            detail (str): The detail of the error, this will usually be shown to the user in the response
            status (int): The http status code for the error.
        """
        self.detail = detail
        self.status = status


class Request:
    def get_json_data_from_request(self, request):
        try:
            return json.loads(request.body.decode('utf-8'))
        except:
            return {}

    def __init__(self, request):
        self.url_name = resolve(request.path_info).url_name
        self.request = request
        self.data = self.get_json_data_from_request(request)
        self.files = request.FILES
        self.method = request.method


def validate_permissions_from_request(request, permission_type, *args, **kwargs):
    """
    This function is responsible for handling and validating permissions directly from the request.
    Usually you will use this function inside of decorators.

    This function works in a way similar like middlewares in django and our custom consumers (check 'reflow_server.core.consumers').

    MOTIVATION:
    This project is built with descentralization in mind. Although it is a Monolithic app, we want to make all of the apps independent from
    each other as deep as possible. With this function you can decentralize the hole permissions case when the user makes a new request. 
    We create the logic to check for a specific permission on one app. Other apps can 'subscribe' to this permission case so everything 
    stays descentralized.

    1 - You create a custom class to handle the permissions. 
    2 - All of the url arguments you want to validate MUST be defined in the __init__ constructor of the class. 
    With this, for every view that recieves a company_id your permission class will recieve this value in it's __init__ function to be validated. 
    3 - So if you want to want to use any argument to validate the permission your class will need to have an __init__ method, this __init__ is the constructor 
    of the class. This constructor will must NOT contain any positional arguments. All arguments must be keyword args. (you can default all of them to None)
    4 - Register it in settings.py PERMISSIONS dict with a custom key, they key must be a list in this case. And the ordering in this list is REALLY
    important.
    5 - When we recieve a request that uses this `validate_permissions_from_request` function we import each class permission that were defined in PERMISSIONS
    in settings.py. When we import this class, we run you class like a function passing a custom request object with some handy arguments. 
    Because of this you NEED to define __call__ method in your classes. The __call__ function must obligatory return a boolean value

    EXAMPLE:
    Okay, so all of this stuff defined above might not be so clear so let's use an example.

    >>> class AuthenticationPermission:
            def __init__(self, company_id=None, user_id=None):
                self.company_id = Encrypt.decrypt_pk(company_id)
                self.user_id = user_id
    
            def __call__(self, request):
                self.user_id = self.user_id if self.user_id else request.request.user.id 
                
                user = UserExtended.objects.filter(id=self.user_id).first()
                company = Company.objects.filter(id=self.company_id).first()

                if not (self.is_valid_compay(company) and self.is_valid_user_company(company, user) and self.is_valid_admin_only_path(user, request.url_name)):
                    raise PermissionsError(detail='invalid', status=404)
    
    The class above is a custom permission class that will validate all of the permissions about authentication. First we define the constructor of this class, so,
    the `__init__` method. This class recieves two arguments in order to create an object: `company_id` and `user_id`. You will notice that both of them defaults
    to None, as said before, you MUST define all of the arguments of your constructor to None. After that, as said before, we call the created object as a function
    sending a custom Request object.

    The arguments you define in your `__init__` constructor method, are the variables you accept on a user request. So if i want to also validate the `notification_id`
    in this class, my `__init__` constructor will be `def __init__(self, company_id=None, user_id=None, notification_id=None):`

    So the second argument of our class is `__call__`. This dunder method in python permits that we run your object as a function. In this method you will see that 
    you recieve a request argument. This request is not the same that you recieve from django, this request object encapsulates the request in another object
    so you can have access other useful stuff for validating permissions. You can see this custom class in `reflow_server.core.permissions.Request`.

    The __call__ dunder function doesn't need to return anything, just validate if the data recieved is valid, so you just raise an 
    `reflow_server.core.permissions.PermissionsError` if anything went wrong.

    After you defining this class, on settings.py you will add something like this:
    >>> PERMISSIONS = {
        'DEFAULT': [
            'reflow_server.authentication.permissions.AuthenticationPermission', # we added on this line
            'reflow_server.authentication.permissions.NotificationPermission'
        ]
    }

    The permissions dict holds can hold as many keys as you want, each key is the `permission_type` str that you send as argument
    to this function. With this we can group the validation not in a single group, but we can actually go through each pipeline
    as we need it. 
    
    Each key is a list containing the module location with the class that we will use to validate. The ordering here is EXTREMELY important
    pretty much like the ordering in django middlewares.

    Args:
        request (django.http.request.HttpRequest): The default request object you usually recieve in your views.
        permission_type (str): The key you want to use in PERMISSIONS variable in `settings.py`, usually the keys
                               in PERMISSIONS is uppercase, but the permissions here can be lowercase

    Raises:
        reflow_server.core.permissions.PermissionsError: if any exception is thrown in the permissions classes, 
        raises this exception.

    Returns:
        bool: Returns True indicating that everything went fine.
    """
    request = Request(request)

    for permission in settings.PERMISSIONS[permission_type.upper()]:
        striped = permission.split('.')
        kls_name = striped.pop(-1)
        path = '.'.join(striped)
        module = __import__(path, fromlist=[kls_name])
        kls = getattr(module, kls_name)

        accepted_keyword_arguments = {}
        # For reference on what i'm doing here https://stackoverflow.com/a/582193
        # we are getting the parameters of the class as a list of strings so we can "subscribe" to recieve these
        # values in the parameter handler class
        for key in list(inspect.signature(kls).parameters):
            accepted_keyword_arguments[key] = kwargs.get(key, None)

        permission_instance = kls(**accepted_keyword_arguments)
        permission_instance(request)

    return True
