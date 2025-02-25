from reflow_server.automation.models import AutomationTrigger, AutomationApp
from reflow_server.formula.services.automation import FlowAutomationService

class TriggerService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id
    
    def activate_trigger(self, app_name, trigger_name, trigger_data={}, debug_trigger=False):
        automation_triggers = AutomationTrigger.objects.filter(
            app_trigger__automation_app__name=app_name, 
            app_trigger__name=trigger_name, 
            automation__company_id=self.company_id
        )
        for automation_trigger in automation_triggers:
            automation_app = AutomationApp.objects.filter(id=automation_trigger.app_trigger.automation_app_id).first()
            flow_script = automation_trigger.app_trigger.script
            flow_automation_service = FlowAutomationService(
                automation_app.flow_context_id,
                self.company_id, 
                self.user_id,
                automation_trigger.automation_id,
                trigger_data=trigger_data,
                debug_trigger=debug_trigger
            )
            flow_automation_service.evaluate(flow_script)