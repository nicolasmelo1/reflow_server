from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct, retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

import requests

from datetime import datetime
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
    def get(url, parameters={}, headers={}, basic_auth=[], **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method':'GET', 
            'url':url, 
            'basic_auth': basic_auth,
            'parameters':parameters,
            'headers': headers
        })

    @functionmethod
    def post(url, data={}, json_data={}, headers={}, basic_auth=[], **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method': 'POST',
            'url': url,
            'data': data,
            'basic_auth': basic_auth,
            'json_data': json_data,
            'headers': headers
        })

    @functionmethod
    def put(url, data={}, json_data={}, headers={}, basic_auth=[], **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method': 'PUT',
            'url': url,
            'data': data,
            'basic_auth': basic_auth,
            'json_data': json_data,
            'headers': headers
        })

    @functionmethod
    def delete(url, parameters={}, headers={}, basic_auth=[], **kwargs):
        request_function = HTTP.request.get_initialized_function(kwargs['__settings__'], 'HTTP', None)
        return request_function._call_({
            'method':'DELETE', 
            'url':url, 
            'parameters':parameters,
            'basic_auth': basic_auth,
            'headers': headers
        })

    @functionmethod
    def request(method, url, parameters={}, data={}, json_data={}, headers={}, basic_auth=[], **kwargs):
        settings = kwargs['__settings__']

        def complex_objects_to_json_serializable(value):
            if isinstance(value, datetime):
                return value.isoformat()
            else:
                return value

        if isinstance(json_data, flow_objects.Dict):
            json_data = json_data._representation_()
            json_data = json.dumps(json_data, default = complex_objects_to_json_serializable)
            json_data = json.loads(json_data)
            
        if isinstance(data, flow_objects.Dict):
            data = data._representation_()

        if isinstance(headers, flow_objects.Dict):
            headers = headers._representation_()

        if isinstance(method, flow_objects.String):
            method = method._representation_()
        
        if isinstance(url, flow_objects.String):
            url = url._representation_()
        
        basic_auth = retrieve_representation(basic_auth)
        if not isinstance(basic_auth, list) or not len(basic_auth) == 2:
            basic_auth = None
        elif isinstance(basic_auth, list):
            basic_auth = tuple(basic_auth)

        headers['User-Agent'] = 'FLOW_HTTP'
        headers['X-Powered-By'] = 'reflow'
        try:
            request_response = requests.request(
                method, url=url, json=json_data, data=data, headers=headers, params=parameters, auth=basic_auth
            )
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
        """
        This is the documentation of the formula, this is required because even if we do not translate the formula documentation directly, we need to have
        any default value so users can know what to do and translators can understand how to translate the formula.
        """
        english_url_definition = {
            'description': 'The url you will make the request to.'
        }
        english_parameters_definition = {
            'description': 'The parameters to send in the url. For example http://example.com?status=perdido. This is the "status=perdido" part',
            'is_required': False
        }
        english_headers_definition = {
            'description': 'This is more advanced, and it is the data you send in the header of the request',
            'is_required': False
        }
        english_data_definition = {
            'description': 'This data is form-encoded, this means it is not a json, this is similar to a formulary data you are sending',
            'is_required': False
        }
        english_json_definition = {
            'description': 'This is the json data you want to send',
            'is_required': False
        }
        english_basic_auth_definition = {
            'description': 'Defines a basic authentication if it has any for the api',
            'is_required': False
        }
        return {
            'description': 'Module for making http requests to external software outside of reflow',
            'methods': {
                'get': {
                    'description': 'Makes GET requests for a given url',
                    'attributes': {
                        'url': english_url_definition,
                        'parameters': english_parameters_definition,
                        'headers': english_headers_definition,
                        'basic_auth': english_basic_auth_definition
                    }
                },
                'delete': {
                    'description': 'Makes DELETE requests for a given url',
                    'attributes': {
                        'url': english_url_definition,
                        'parameters': english_parameters_definition,
                        'headers': english_headers_definition,
                        'basic_auth': english_basic_auth_definition
                    }
                },
                'post': {
                    'description': 'Makes POST requests for a given url with some data on the JSON format or Form encoded.',
                    'attributes': {
                        'url': english_url_definition,
                        'data': english_data_definition,
                        'json_data': english_json_definition,
                        'headers': english_headers_definition,
                        'basic_auth': english_basic_auth_definition
                    }
                },
                'put': {
                    'description': 'Makes PUT requests for a given url with some data on the JSON format or Form encoded.',
                    'attributes': {
                        'url': english_url_definition,
                        'data': english_data_definition,
                        'json_data': english_json_definition,
                        'headers': english_headers_definition,
                        'basic_auth': english_basic_auth_definition
                    }
                },
                'request': {
                    'description': 'Created for advanced users that are in a hole other level, like you. Makes a request for any method you like for a given url.',
                    'attributes': {
                        'method': {
                            'description': 'A "PUT, POST, GET, DELETE, OPTION, etc." method type string.',
                        },
                        'url': english_url_definition,
                        'parameters': english_parameters_definition,
                        'data': english_data_definition,
                        'json_data': english_json_definition,
                        'headers': english_headers_definition,
                        'basic_auth': english_basic_auth_definition
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
                        },
                        'content': {
                            'description': 'This is a string of the content recieved. If the requests sends a string you should use this',
                        },
                        'json': {
                            'description': 'The json data of the request made, this will be generally used for most APIs',
                        }
                    }
                }
            }
        }