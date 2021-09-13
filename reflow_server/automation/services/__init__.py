from reflow_server.automation.models import AutomationTrigger


class AutomationService:
    def __init__(self, company_id):
        self.company_id = company_id

    def trigger(self, app_name, trigger_name):
        automation_trigger = AutomationTrigger.objects.filter(
            app_trigger__automation_app__name=app_name, 
            app_trigger__name=trigger_name, 
            automation__company_id=self.company_id
        )
        formula = automation_trigger.app_trigger.script
        