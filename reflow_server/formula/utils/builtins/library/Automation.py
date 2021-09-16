from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects
from reflow_server.formula.utils.helpers import Conversor

from datetime import datetime


class Automation(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def get_data(**kwargs):
        settings = kwargs['__settings__']

        if settings.reflow_automation_trigger_data != None:
            data = settings.reflow_automation_trigger_data
        else:
            data = settings.reflow_automation_action_data

        conversor = Conversor(settings)
        return conversor.python_value_to_flow_object(data)

    @functionmethod
    def trigger_action(data, **kwargs):
        settings = kwargs['__settings__']

        data = retrieve_representation(data)

        if settings.reflow_automation_trigger_data != None:
            if isinstance(data, dict) and all([
                isinstance(value, str) or 
                isinstance(value, int) or 
                isinstance(value, bool) or
                isinstance(value, float) or 
                isinstance(value, bytes) or
                isinstance(value, datetime) or 
                value == None 
                for value in data.values()
            ]):
                from reflow_server.automation.services.actions import ActionService

                settings = kwargs['__settings__']
                action_service = ActionService(settings.reflow_company_id, settings.reflow_user_id)
                action_service.trigger_action(settings.reflow_automation_id, data)
            else:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'The data sent needs to be a flat dict, lists and dicts are not accepted')
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Function available inside triggers only')

    def _documentation_(self):
        return {
            'description': 'Flow module created to be used inside of the automation only, this is not available in the formulary',
        }