from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct
from reflow_server.formula.utils.builtins import objects as flow_objects

import requests

import urllib.error
import urllib.request
import urllib.parse
import json


class HTTPResponse(LibraryStruct):
    """
    Class ressponsible for evaluating the responses of the request, you can retrieve it as content, or as JSON by now.
    """
    def __init__(self, settings, response, decode_format='utf-8'):
        self.status_code = response.status_code
        self.content = response.content.decode(decode_format)
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
    def get(url, parameters={}, headers={}, **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method':'GET', 
            'url':url, 
            'parameters':parameters,
            'headers': headers
        })

    @functionmethod
    def post(url, data={}, json={}, headers={}, **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method': 'POST',
            'url': url,
            'data': data,
            'json_data': json,
            'headers': headers
        })

    @functionmethod
    def put(url, data, json, headers={}, **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method': 'PUT',
            'url': url,
            'data': data,
            'json_data': json,
            'headers': headers
        })

    @functionmethod
    def delete(url, parameters, headers={}, **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method':'DELETE', 
            'url':url, 
            'parameters':parameters,
            'headers': headers
        })

    @functionmethod
    def request(method, url, parameters={}, data={}, json_data={}, headers={}, **kwargs):
        settings = kwargs['__settings__']

        if isinstance(json_data, flow_objects.Dict):
            json_data = json_data._representation_()

        if isinstance(data, flow_objects.Dict):
            data = data._representation_()

        if isinstance(headers, flow_objects.Dict):
            headers = headers._representation_()

        if isinstance(method, flow_objects.String):
            method = method._representation_()
        
        if isinstance(url, flow_objects.String):
            url = url._representation_()
        
        headers['User-Agent'] = 'FLOW_HTTP'
        headers['X-Powered-By'] = 'reflow'

        try:
            request_response = requests.request(method, url=url, json=json_data, data=data, headers=headers, params=parameters)
            response = HTTPResponse(
                settings=settings,
                response=request_response
            )
        except Exception as e:
            response = HTTPResponse(
                settings=settings,
                response=e
            )
        return response
    
    def _documentation_(self):
        english_url_definition = {
            'description': 'The url you will make the request to.',
            'type': 'String'
        }
        english_parameters_definition = {
            'description': 'The parameters to send in the url. For example http://example.com?status=perdido. This is the "status=perdido" part',
            'type': 'Dictionary'
        }
        english_headers_definition = {
            'description': 'This is more advanced, and it is the data you send in the header of the request',
            'type': 'Dictionary'
        }
        english_data_definition = {
            'description': 'This data is form-encoded, this means it is not a json, this is similar to a formulary data you are sending',
            'type': 'Dictionary'
        }
        english_json_definition = {
            'description': 'This data is form-encoded, this means it is not a json, this is similar to a formulary data you are sending',
            'type': 'Dictionary'
        }
        return {
            'english': {
                'definition': 'Module for making http requests to external software outside of reflow',
                'methods': {
                    'get': {
                        'description': 'Makes GET requests for a given url',
                        'attributes': {
                            'url': english_url_definition,
                            'parameters': english_parameters_definition,
                            'headers': english_headers_definition
                        }
                    },
                    'delete': {
                        'description': 'Makes DELETE requests for a given url',
                        'attributes': {
                            'url': english_url_definition,
                            'parameters': english_parameters_definition,
                            'headers': english_headers_definition
                        }
                    },
                    'post': {
                        'description': 'Makes POST requests for a given url with some data on the JSON format or Form encoded.',
                        'attributes': {
                            'url': english_url_definition,
                            'data': english_data_definition,
                            'json_data': english_json_definition,
                            'headers': english_headers_definition
                        }
                    },
                    'put': {
                        'description': 'Makes PUT requests for a given url with some data on the JSON format or Form encoded.',
                        'attributes': {
                            'url': english_url_definition,
                            'data': english_data_definition,
                            'json_data': english_json_definition,
                            'headers': english_headers_definition
                        }
                    },
                    'request': {
                        'description': 'Created for advanced users that are in a hole other level, like you. Makes a request for any method you like for a given url.',
                        'attributes': {
                            'method': {
                                'description': 'A "PUT, POST, GET, DELETE, OPTION, etc." method type.',
                                'type': 'String'
                            },
                            'url': english_url_definition,
                            'data': english_data_definition,
                            'json_data': english_json_definition,
                            'headers': english_headers_definition
                        }
                    }
                },
                'structs': {
                    'HTTPResponse': {
                        'description': 'After you make a request this Struct is returned so you can use to query your data. So for example, after this code runs '
                                       '`response = HTTP.get("www.reflow.com.br")`. You can view the content of the page by making `response.content`, or the status code'
                                       'by making `response.status_code`',
                        'attributes': {
                            'status_code': {
                                'description': 'The HTTP status code of the request',
                                'type': 'Integer'
                            },
                            'content': {
                                'description': 'This is a string of the content recieved. If the requests sends a string you should use this',
                                'type': 'String'
                            },
                            'json': {
                                'description': 'The json data of the request made, this will be generally used for most APIs',
                                'type': 'Dictionary'
                            }
                        }
                    }
                }
            }
        }