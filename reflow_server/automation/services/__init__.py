from reflow_server.automation.models import AutomationTrigger
from reflow_server.formula.services.formula import FlowFormulaService
from reflow_server.automation.services.triggers import TriggerService


class AutomationService:
    def __init__(self, company_id):
        self.company_id = company_id

    def trigger(self, user_id, app_name, trigger_name, trigger_data):
        trigger_service = TriggerService(company_id=self.company_id, user_id=user_id)
        trigger_service.activate_trigger(app_name, trigger_name, trigger_data)