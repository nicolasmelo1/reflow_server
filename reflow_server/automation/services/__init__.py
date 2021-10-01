from reflow_server.automation.models import AutomationTrigger
from reflow_server.formula.services.formula import FlowFormulaService
from reflow_server.automation.services.triggers import TriggerService
from reflow_server.core.utils.asynchronous import RunAsyncFunction


class AutomationService:
    def __init__(self, company_id):
        """
        Class responsible for handling simple automation services, right now this handle only the triggers
        when a webhook is called or an event is called it is here were we send those automations.

        We DO NOT handle Reflow specific logic here, for example, when a formulary is created or if a formulary is updated
        for that we have the ReflowAutomationService in `reflow_server.automation.services.reflow.ReflowAutomationService`
        """
        self.company_id = company_id

    def trigger(self, user_id, app_name, trigger_name, trigger_data={}, debug_trigger=False):
        trigger_service = TriggerService(company_id=self.company_id, user_id=user_id)
        async_function = RunAsyncFunction(trigger_service.activate_trigger)
        async_function.delay(
            app_name=app_name, 
            trigger_name=trigger_name, 
            trigger_data=trigger_data, 
            debug_trigger=debug_trigger
        )