from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct
from reflow_server.formula.utils.builtins import objects as flow_objects

import urllib.error
import urllib.request
import urllib.parse
import json


class HTTPResponse(LibraryStruct):
    """
    Class ressponsible for evaluating the responses of the request, you can retrieve it as content, or as JSON by now.
    """
    def __init__(self, settings, response, decode_format='utf-8'):
        self.status_code = response.code
        self.content = response.read().decode(decode_format)
        try:
            self.json = json.loads(self.content)
        except Exception as e:
            self.json = None
        super().__init__('HTTP', settings)


class HTTP(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def get(url, parameters, headers={}):
        pass

    @functionmethod
    def post(url, data, headers={}):
        pass

    @functionmethod
    def put(url, data, headers={}):
        pass

    @functionmethod
    def delete(url, parameters, headers={}):
        pass

    @functionmethod
    def request(method, url, parameters={}, data={}, headers={}, **kwargs):
        settings = kwargs['__settings__']
        if isinstance(headers, flow_objects.Dict):
            headers = headers._representation_()

        if isinstance(method, flow_objects.String):
            method = method._representation_()
        
        if isinstance(url, flow_objects.String):
            url = url._representation_()
        
        headers['User-Agent'] = 'flow_http'
        request = urllib.request.Request(url=url, data=data, headers=headers)
        request.get_method = lambda: method.upper()
        try:
            request_response = urllib.request.urlopen(request)
            response = HTTPResponse(
                settings=settings,
                response=request_response
            )
        except urllib.error.HTTPError as httpe:
            response = HTTPResponse(
                settings=settings,
                response=httpe
            )
        return response