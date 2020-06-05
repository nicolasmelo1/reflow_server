from django.conf import settings

from reflow_server.core.services.external import ExternalService

import requests

class External:
    """
    Okay, so this class is used as the base for externals. It is not that difficult but can be tricky to follow along.

    Your externals needs to always inherit from this class. It exposes `.post()`, `.get()`, `.put()` and `.delete()` operations
    for your class.

    The `host` must be defined in your class.
    The `secure` is used if your application is communicating with another reflow application and must be defined in your class.

    You can also use `secure` on each request, if you are communicating to non Reflow applications.
    """
    host = ''
    secure = True

    def __make_request(self, method, url, secure=True, headers=None, params=None, data=None):
        """
        This method is hidden from outside of this class, it's used to fire a request using requests library.
        It's important to understand that the request fails silently in development, but not in production.

        Arguments:
            method {str} -- The request method, can be `PUT`, `POST`, `GET` or `DELETE`
            url {str} -- The path of your request.

        Keyword Arguments:
            secure {bool} -- Use True if you are communicating to a Reflow app and False otherwise (default: {True})
            headers {dict} --  The header of your request (default: {None})
            params {dict} -- Custom query param (default: {None})
            data {dict} -- The data to be sent on `PUT` or `POST` requests (default: {None})

        Raises:
            ce: If this app is in production, we raise the exception on the request, otherwise
                we fail silently.

        Returns:
            requests.Response -- Returns the response of the request. For further documentation refer to:
                                 https://requests.readthedocs.io/en/master/user/quickstart/#response-content 
        """
        try:
            if (secure or self.secure) and not headers:
                return requests.request(method=method, url=self.host + url, headers=ExternalService.authorize_request(), params=params, json=data)
            return requests.request(method=method, url=self.host + url, headers=headers, params=params, json=data)

        except requests.exceptions.ConnectionError as ce:
            if settings.ENV == 'server':
                raise ce
        
    def get(self, url, params=None, secure=True, headers=None):
        return self.__make_request('GET', url, params=params, headers=headers, secure=secure)
        
    def post(self, url, data=None, secure=True, headers=None):
        return self.__make_request('POST', url, data=data, headers=headers,secure=secure)

    def put(self, url, data=None, secure=True, headers=None):
        return self.__make_request('PUT', url, data=data, headers=headers,secure=secure)

    def delete(self, url, params=None, secure=True, headers=None):
        return self.__make_request('DELETE', url, params=params, headers=headers,secure=secure)