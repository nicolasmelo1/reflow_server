from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects


class Reflow(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def debug(element, **kwargs):
        print(element)
        return flow_objects.Null(kwargs['__settings__'])._initialize_()
    
    @functionmethod
    def create_record(template_name, page_name, data, **kwargs):
        from reflow_server.formula.services.reflow_module import ReflowModuleService, ReflowModuleServiceException
        settings = kwargs['__settings__']
        
        template_name = retrieve_representation(template_name)
        page_name = retrieve_representation(page_name)
        data = retrieve_representation(data)
        
        try:
            reflow_module_service = ReflowModuleService(
                settings.reflow_company_id, 
                settings.reflow_user_id, 
                settings.reflow_dynamic_form_id
            )
            formulary_record_id = reflow_module_service.create_record(template_name, page_name, data)
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(formulary_record_id)
        except ReflowModuleServiceException as rmse:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', str(rmse))
    
    def _documentation_(self):
        return {
            'description': 'Creates an api that enables users to work and manage reflow inside of the formulas',
            'methods': {
                'create_record': {
                    'description': 'Creates a new record in a page',
                    'attributes': {
                        'template_name': {
                            'description': 'The name of the template the "page_name" is from',
                            'is_required': True
                        },
                        'page_name': {
                            'description': 'The name of the page that you will be creating this new record',
                            'is_required': True
                        },
                        'data': {
                            'description': 'The data to add should follow this format:\n'
                                           '>>> {\n'
                                           '    "Name of The section": {\n'
                                           '        "Name of the field": [{{Your value}}]\n'    
                                           '    },\n'
                                           '    "Name of the multi-section": [\n'
                                           '        {\n'
                                           '            "Name of the field": [{{Your value}}]\n'    
                                           '        }\n'
                                           '    ]\n'
                                           '}\n',
                            'is_required': True
                        }
                    }
                }
            }
        }