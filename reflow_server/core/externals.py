from django.conf import settings

from reflow_server.core.services.external import ExternalService

import requests
import logging


class External:
    """
    This class is used as the base for externals. It is not that difficult but can be tricky to follow along.

    Your externals needs to always inherit from this class. It exposes `.post()`, `.get()`, `.put()` and `.delete()` operations
    for your class.

    IMPORTANT: since you usually have serializers in your externals, and externals are called from services that are also used in serializers, 
    most of the time your externals might need to be imported right when you use it and not on the top of the file as you might be familiar with.

    Class Attributes:
        - `host` MUST be defined in your class.
        - `secure` is used if your application is communicating with another Reflow application inside reflow's ecosystem.
        - `basic_auth` simple tuple to be used as basic authentication, with this `secure` must be defined in your class and set to False.
        refer to https://requests.readthedocs.io/pt_BR/latest/user/authentication.html for reference.
    
    You can also use `secure` on each request, if you are communicating to non Reflow applications.
    """
    host = ''
    secure = True
    basic_auth = None

    def __make_request(self, method, url, secure=True, headers=None, params=None, data=None):
        """
        This method is hidden from outside of this class, it's used to fire a request using requests library.
        It's important to understand that the request fails silently in development, but not in production.

        Args:
            method (str): The request method, can be `PUT`, `POST`, `GET` or `DELETE`
            url (str): The path of your request.
            secure (bool, optional): Use True if you are communicating to a Reflow app and False otherwise. Defaults to True.
            headers (dict, optional): The header of your request. Defaults to None.
            params (dict, optional): Custom query param. Defaults to None.
            data (dict, optional): The data to be sent on `PUT` or `POST` requests. Defaults to None.

        Raises:
            ce: If this app is in production, we raise the exception on the request, otherwise
                we fail silently.

        Returns:
            requests.Response: Returns the response of the request. For further documentation refer to:
                               https://requests.readthedocs.io/en/master/user/quickstart/#response-content         
        """
        try:
            basic_auth = self.basic_auth if not self.secure else None

            if (secure or self.secure) and not headers:
                return requests.request(method=method, url=self.host + url, headers=ExternalService.authorize_request(), params=params, json=data, auth=basic_auth)
            return requests.request(method=method, url=self.host + url, headers=headers, params=params, json=data, auth=basic_auth)

        except requests.exceptions.ConnectionError as ce:
            if settings.ENV == 'server':
                raise ce
            else:
                logging.warn('Tried to connect to host: {} but could not establish a connection. Check if the host is up and running.'.format(self.host + url))
        
    def get(self, url, params=None, secure=True, headers=None):
        return self.__make_request('GET', url, params=params, headers=headers, secure=secure)
        
    def post(self, url, data=None, secure=True, headers=None):
        return self.__make_request('POST', url, data=data, headers=headers, secure=secure)

    def put(self, url, data=None, secure=True, headers=None):
        return self.__make_request('PUT', url, data=data, headers=headers, secure=secure)

    def delete(self, url, params=None, secure=True, headers=None):
        return self.__make_request('DELETE', url, params=params, headers=headers,secure=secure)