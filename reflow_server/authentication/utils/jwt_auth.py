from django.conf import settings
from datetime import datetime, timedelta
import jwt


class JWT:
    def __init__(self, jwt=None):
        """
        This class is used for JWT handling in our application. There are two use cases to use this class:
        
        1 - Create a new jwt token (refresh token or authentication token)
        2 - validate the jwt token

        For the first case this class exposes two methods: `.get_token(user_id)` and `.get_refresh_token(user_id)`. 
        For both of them you need to pass the user_id argument in order to create a token.
        Since they are both staticmethods you don't need a object of the class.

        For the second case you may want to create a object of this class and then call the method
        `.extract_jwt_from_request(request)`. Then you need to call `.is_valid()` function. 

        IMPORTANT:
        After you call `.is_valid()` if your data is valid the `.data` property will contain your data.
        After you call `.is_valid()` if your data IS NOT VALID the `.error` property will contain your errors
        """
        self.jwt = jwt

    @property
    def invalid_token_error(self):
        """
        We use this to mantain the consistency on the error messages if we want to fire the
        error outside this class

        Returns:
            str -- the error message if the token is invalid
        """
        return 'invalid_token'
    
    @property
    def expired_token_error(self):
        return 'expired_token'
    
    @property
    def unknown_error(self):
        return 'unknown_error'

    def __validate_jwt_token(self):
        if not self.jwt:
            self._error = 'jwt_not_defined'
            return False
        
        header = self.jwt
        for jwt_header_type in settings.JWT_HEADER_TYPES:
            header = header.replace(jwt_header_type, '')
        header = header.replace(' ','')
        try:
            payload = jwt.decode(str(header), settings.SECRET_KEY, algorithms=[settings.JWT_ENCODING])
            self._data = payload
            return True

        except (jwt.exceptions.DecodeError, jwt.exceptions.InvalidSignatureError) as error:
            self._error = self.invalid_token_error
            return False

        except jwt.exceptions.ExpiredSignatureError as error:
            self._error = self.expired_token_error
            return False
        
        except Exception as e:
            self._error = self.unknown_error
            return False


    def is_valid(self):
        """
        Checks if a jwt token is valid. .jwt must be defined prior on calling this function. You could define it
        either on the object initialization, or use the `.extract_jwt_from_scope()` or `.extract_jwt_from_request()`
        to extract the jwt for either the scope of the request.

        Raises:
            AssertionError: if the jwt is not valid

        Returns:
            bool -- True or False depending if the user is valid or not
        """
        if not hasattr(self, 'jwt'):
            raise AssertionError('You must extract the jwt token from the request before calling `.is_valid()`')

        return self.__validate_jwt_token()


    @property
    def data(self):
        """
        Gets the data encoded in the jwt token.

        Raises:
            AssertionError: If `.is_valid()` is not called prior to calling `.data`
            AssertionError: If `.is_valid()` is false, you will not be able to call `.data`

        Returns:
            dict -- a dict containing your encoded data.
        """
        if not hasattr(self, '_data') and not hasattr(self, '_error'):
            msg = 'You must call `.is_valid()` before trying to retrieve the data'
            raise AssertionError(msg)
        elif hasattr(self, '_error'):
            msg = 'Looks like your jwt token was not valid. Call `.error` to retrieve the validation error'
            raise AssertionError(msg)
        else:
            return self._data

    @property
    def error(self):
        """
        Retrieves the error message if your jwt token is not valid.

        Raises:
            AssertionError: If `.is_valid()` is not called prior to calling `.error`
            AssertionError: If `.is_valid()` is True, you will not be able to call `.error`

        Returns:
            [type] -- [description]
        """
        if not hasattr(self, '_data') and not hasattr(self, '_error'):
            msg = 'You must call `.is_valid()` before trying to retrieve the errors'
            raise AssertionError(msg)
        elif hasattr(self, '_data'):
            msg = 'Why are you trying to get the errors if everything went fine? ' + \
                  'Call `.data` to retrieve the payload of your jwt'
            raise AssertionError(msg)
        else:
            return self._error

    def extract_jwt_from_scope(self, scope):
        """
        Takes out the jwt token from the Django Consumer scope

        Arguments:
            scope {dict} -- Django consumer scope
        """
        if 'query_string' in scope and 'token=' in str(scope['query_string']):
            self.jwt = scope['query_string'].decode('utf-8').replace('token=', '')

    def extract_jwt_from_request(self, request):
        """
        Takes out the jwt token from the Django request. The token can be either on a header or a GET parameter as `token`

        Arguments:
            request {django.Request} -- django request.
        """
        if 'HTTP_AUTHORIZATION' in request.META or 'token' in request.GET:
            self.jwt = request.META['HTTP_AUTHORIZATION'] if 'HTTP_AUTHORIZATION' in request.META else request.GET['token']

    @staticmethod
    def get_token(user_id):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 24 hours into the future.

        Arguments:
            user_id {int} -- The user id to be encoded on the token
        """
        dt = datetime.now() + timedelta(hours=24)

        token = jwt.encode({
            'id': user_id,
            'exp': int(dt.strftime('%s')),
            'type': 'access'
        }, settings.SECRET_KEY, algorithm=settings.JWT_ENCODING)

        return token.decode('utf-8')


    @staticmethod
    def get_refresh_token(user_id):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.

        Arguments:
            user_id {int} -- the user id to be enconded inside of the token.
        """
        dt = datetime.now() + timedelta(days=60)

        refresh_token = jwt.encode({
            'id': user_id,
            'exp':int(dt.strftime('%s')),
            'type': 'refresh'
        }, settings.SECRET_KEY, algorithm=settings.JWT_ENCODING)
        return refresh_token.decode('utf-8')

    