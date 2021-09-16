from reflow_server.automation.models import AutomationAction, AutomationAction


class ActionService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id

    def trigger_action(self, automation_id, trigger_data):
        automation_actions = AutomationAction.objects.filter(
            automation_id=automation_id, 
        )

        for automation_action in automation_actions:
            print(automation_action)
        
        
    def retrieve_data(self, automation_id):
        automation_triggers = AutomationAction.objects.filter(
            id=automation_id
        )
        return {}