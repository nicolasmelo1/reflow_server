from django.http import HttpResponse


class Cors:
    """
    Class created for handling CORS. Like explained in reflow_server.core.middleware.CorsMiddleware i was using
    the django-cors library. But seeing the source code, everything looks easy enough to implement it by hand.
    """
    OPTIONS_METHOD = 'OPTIONS'
    ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
    ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
    ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
    ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
    ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"

    DEFAULT_CORS_PREFLIGHT_MAX_AGE = 86400
    DEFAULT_ACCEPTED_HEADERS = ["accept","accept-encoding","authorization","content-type","dnt","origin","user-agent","x-csrftoken","x-requested-with"]
    DEFAULT_ACCEPTED_METHODS = ["DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT"]

    def is_preflight(self, request):
        """
        The stuff starts mostly here if you see. With CORS the browser AUTOMATICALLY sends an OPTION request
        to the server to see all of the cors configuration from the server.

        Args:
            request (django.http.HttpRequest): The Request object from django recieved on the middleware.

        Returns:
            bool: If it is a pre flight (so the browser checking for our backend configuration) we return true, 
            otherwise we return False
        """
        if hasattr(request, 'method') and request.method == self.OPTIONS_METHOD:
            return True
        else:
            return False

    def handle_preflight(self, request):
        """
        When the request is the preflight option request, what we do is send an empty response wthout the actual data so
        it's faster to send the response.

        Args:
            request (django.http.HttpRequest): The Request object from django recieved on the middleware.

        Returns:
            django.http.HttpResponse: Returns an HttpResponse object to the client
        """
        response = HttpResponse()
        response["Content-Length"] = "0"
        response[self.ACCESS_CONTROL_MAX_AGE] = self.DEFAULT_CORS_PREFLIGHT_MAX_AGE
        response[self.ACCESS_CONTROL_ALLOW_METHODS] = ', '.join(self.DEFAULT_ACCEPTED_METHODS)
        response[self.ACCESS_CONTROL_ALLOW_HEADERS] = ', '.join(self.DEFAULT_ACCEPTED_HEADERS)
        response[self.ACCESS_CONTROL_ALLOW_CREDENTIALS] = "true"
        response = self.add_allow_origin_to_response(request, response)
        return response

    def add_allow_origin_to_response(self, request, response):
        origin = request.META.get("HTTP_ORIGIN")
        response[self.ACCESS_CONTROL_ALLOW_ORIGIN] = origin
        return response

    def handle_cors(self, request, response):
        if self.is_preflight(request):
            return self.handle_preflight(request)
        else:
            return self.add_allow_origin_to_response(request, response)