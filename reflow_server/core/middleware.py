from reflow_server.core.utils.cors import Cors


class CORSMiddleware:
    """
    With this we can control how cors works, i was actually using django-cors and most of this
    was inspired by this lib. But i saw the source code and thought everything was too simple and i could 
    definetly do something like that by myself without the need of an external lib
    """
    def __init__(self, get_response):
        self.cors = Cors()
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        return self.cors.handle_cors(request, response)

