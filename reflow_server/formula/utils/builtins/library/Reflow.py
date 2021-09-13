from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod
from reflow_server.formula.utils.builtins import objects as flow_objects


class Reflow(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def create_record(template_name, page_name, data, **kwargs):
        from reflow_server.formula.services.reflow_module import ReflowModuleService, ReflowModuleServiceException

        settings = kwargs['__settings__']

        if isinstance(page_name, flow_objects.String):
            page_name = page_name._representation_()

        if isinstance(data, flow_objects.Dict):
            data = data._representation_()
        
        try:
            reflow_module_service = ReflowModuleService(
                settings.reflow_company_id, 
                settings.reflow_user_id, 
                settings.reflow_dynamic_form_id
            )
            return reflow_module_service.create_record(template_name, page_name, data)
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