from reflow_server.automation.models import AutomationAction, AutomationAction, AutomationApp, \
    AutomationDebugTriggerData, AutomationTrigger
from reflow_server.formula.services.automation import FlowAutomationService

import json


class ActionService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id

    def trigger_action(self, automation_id, action_data_from_trigger, debug_trigger=False):
        """
        This triggers an action. Triggering an action is nothing more that triggering a flow script
        with this flow script we are able to create records, update records and do almost anything
        imaginable by us.

        Args:
            automation_id (int): The automation instance id, this is the id of this particular automation.
            BEWARE, it is NOT the automation_app it is the automation, the automation that is bounded to each
            company.
            action_data_from_trigger (dict): The data recieved from the trigger. Every trigger sends a data, even though
            they can be empty, but they always need to send something. This can be the data from the e-mail you recieved
            or the data from the reflow record you added and so on.
            debug_trigger (bool, optional): Used for debugging purposes, for the user. When the user is setting up an automation.
            the trigger data might not be known before hand. Defaults to False.
        """
        if debug_trigger:
            debug_data_id = AutomationTrigger.automation_.debug_data_id_by_automation_id(automation_id)
            data_from_trigger_stringfied = json.dumps(action_data_from_trigger)
            AutomationDebugTriggerData.automation_.create_or_update_debug_trigger_data(data_from_trigger_stringfied, debug_data_id)
        else:
            automation_actions = AutomationAction.objects.filter(
                automation_id=automation_id, 
            )
            automation = AutomationApp.objects.filter(id=automation_id).first()

            for automation_action in automation_actions:
                if automation_action.custom_script not in ['', None]:
                    flow_script = automation_action.custom_script
                else:
                    flow_script = automation_action.app_action.script

                flow_automation_service = FlowAutomationService(
                    automation.flow_context_id,
                    self.company_id, 
                    self.user_id,
                    automation_id,
                    action_data=action_data_from_trigger
                )
                result = flow_automation_service.evaluate(flow_script)