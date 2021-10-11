from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects
from reflow_server.formula.utils.builtins.objects.Integer import Integer


class List(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def range(start, end, steps=1, **kwargs):
        def is_valid_parameter(parameter):
            return isinstance(parameter, flow_objects.Integer) or \
                isinstance(parameter, int)

        start = retrieve_representation(start)
        end = retrieve_representation(end)
        steps = retrieve_representation(steps)

        is_valid_start = is_valid_parameter(start)
        is_valid_end = is_valid_parameter(end)
        is_valid_steps = is_valid_parameter(steps)
        if is_valid_start and is_valid_end and is_valid_steps and steps != 0:
            new_range = [flow_objects.Integer(kwargs['__settings__'])._initialize_(element) for element in range(start, end, steps)]
            
            new_list = flow_objects.List(kwargs['__settings__'])
            return new_list._initialize_(new_range)
        elif steps == 0:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "`steps` cannot be 0")
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "`start`, `end` or `step` should be an integer")


    @functionmethod
    def length(list_data, **kwargs):
        list_data = retrieve_representation(list_data)

        if isinstance(list_data, list):
            size = len(list_data)

            result = flow_objects.Integer(kwargs['__settings__'])
            return result._initialize_(size)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "'list_data' should be a list")

    @functionmethod
    def append(list_data, element, **kwargs):
        if not isinstance(list_data, flow_objects.List):
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "'list_data' should be a list")
        if not isinstance(element, flow_objects.Object):
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "'element' is invalid")

        list_data.array.append(element)     

        return element

    @functionmethod
    def for_each(list_data, function, **kwargs):
        if not isinstance(list_data, flow_objects.List):
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "'list_data' should be a list")

        if not isinstance(function, flow_objects.Function):
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', "'function' should be a function to run for each element in the list")

        for index in range(0, list_data.array.number_of_elements):
            element = list_data._getitem_(index)
            parameters = {}
            for parameter_index, parameter in enumerate(function.parameters):
                if parameter_index == 0:
                    parameters[parameter[0]] = element
                elif parameter_index == 1:
                    parameters[parameter[0]] = flow_objects.Integer(kwargs['__settings__'])._initialize_(index)
            
            function._call_(parameters)

        return flow_objects.Null(kwargs['__settings__'])._initialize_()
    
    @functionmethod
    def map(list_data, function, **kwargs):
        new_list = flow_objects.List(kwargs['__settings__'])
        new_list._initialize_([])
        for index in range(0, list_data.array.number_of_elements):
            element = list_data._getitem_(index)
            parameters = {}
            for parameter_index, parameter in enumerate(function.parameters):
                if parameter_index == 0:
                    parameters[parameter[0]] = element
                elif parameter_index == 1:
                    parameters[parameter[0]] = flow_objects.Integer(kwargs['__settings__'])._initialize_(index)

            result = function._call_(parameters)
            new_list.array.append(result)

        return new_list

    def _documentation_(self):
        """
        This is the documentation of the formula, this is required because even if we do not translate the formula documentation directly, we need to have
        any default value so users can know what to do and translators can understand how to translate the formula.
        """
        return {
            "description": "List module is responsible for handling stuff in lists, with this we are able to do many operations inside of lists like retrieving the length,"
                           "lopping through all elements in a map or a for_each and so on.",
            "methods": {
                "length": {
                    'description': 'Finds the length of a list, returns a number. Example: \n'
                                   '>>> list = [1,2,3]\n'
                                   '>>> List.length(list) # 3',
                    'attributes': {
                        'list_data': {
                            'description': 'The list to find the length to',
                            'is_required': True
                        }
                    }
                },
                "range": {
                    'description': 'Creates a new list from start to finish and by each step. Example:\n'
                                   '>>> List.range(0, 5) == [0, 1, 2, 3, 4]\n'
                                   '>>> List.range(0, 5, 2) == [0, 2, 4]\n'
                                   '>>> List.range(5, 1, -1) == [5, 4, 3, 2]\n',
                    'attributes': {
                        'start': {
                            'description': 'A number, that should be an integer of where the list starts, from what number the list starts counting',
                            'is_required': True,
                        },
                        'end': {
                            'description': 'A number, that should be an integer of where the list ends, from what number the list end counting. '
                                           'The end IS NOT CONSIDERED, so if you want the 5 to be on the list you should pass the value 6.',
                            'is_required': True,
                        },
                        'steps': {
                            'description': 'A number, this is each step of the list, if you add 2, it will skip 2 for all values, so, [1, 3, 5] and so on. Defaults to 1.',
                            'is_required': False,
                        }
                    }
                },
                "append": {
                    'description': 'Appends a new element to a list. Example: \n'
                                   '>>> list = []\n'
                                   '>>> List.append(list, 3)\n'
                                   '>>> list # [3]',
                    'attributes': {
                        'element': {
                            'description': 'The element you want to add in the list, there is not requirements here.',
                            'is_required': True
                        }
                    }
                },
                "for_each": {
                    'description': "Loop though all elements of a list, it does not expect any output, the function passed will recieve 'element' and/or 'index' parameters. Example: \n"
                                   '>>> list = ["1", "2", "3"]\n'
                                   ">>> List.for_each(list, function(element) do\n"
                                   '        HTTP.post("https://api.example.com/post/" + element, json_data={})    '
                                   "    end)\n",
                    'attributes': {
                        'list_data': {
                            'description': 'The list to loop through',
                            'is_required': True
                        },
                        'function': {
                            'description': 'The function that will run for every element on the list, it recieves a "element" and "index" parameters.'
                                           'notice that both parameters are positional, so the first parameter will be ALWAYS "element", and the second' 
                                           'will ALWAYS be "index", also notice that both parameters are optional',
                            'is_required': True
                        }
                    }
                },
                "map": {
                    'description': "Loop though all elements of a list, expect a new list as output, the function passed will recieve 'element' and/or 'index' parameters. Example: \n"
                                   '>>> list = ["1", "2", "3"]\n'
                                   ">>> List.for_each(list, function(element) do\n"
                                   '        HTTP.post("https://api.example.com/post/" + element, json_data={})    '
                                   "    end)\n",
                    'attributes': {
                        'list_data': {
                            'description': 'The list to loop through',
                            'is_required': True
                        },
                        'function': {
                            'description': 'The function that will run for every element on the list, it recieves a "element" and "index" parameters.'
                                           'notice that both parameters are positional, so the first parameter will be ALWAYS "element", and the second' 
                                           'will ALWAYS be "index", also notice that both parameters are optional',
                            'is_required': True
                        }
                    }
                }
            }
        }