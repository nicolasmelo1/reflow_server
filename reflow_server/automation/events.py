from reflow_server.automation.services.reflow import ReflowAutomationService


class AutomationEvent:
    # ------------------------------------------------------------------------------------------
    def formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public, data):
        """
        This event is fired when the a new record is created in the formulary. So the formulary is created but when we add
        new data to it.

        Args:
            user_id (int): The UserExtended instance id of the user. This is the user that added new data. Remember that public
                           formulary also has the id of the user, so we have the 'is_public' to know that it is a public formulary.
            company_id (int): The Company instance id on what company does this formulary data was added. 
            form_id (int): The Form instance id, on what formulary this data was added. 
            form_data_id (int): What was the data added. 
            is_public (bool): Is it a public formulary or not?
        """
        reflow_automation_service = ReflowAutomationService(company_id, user_id)
        reflow_automation_service.formulary_data_created(form_id, form_data_id, data)
    # ------------------------------------------------------------------------------------------
    def formulary_data_updated(self, user_id, company_id, form_id, form_data_id, is_public, data):
        """
        Similar to `.formulary_data_created()` except it works when the data was updated in a formulary.

        Args:
            user_id (int): The UserExtended instance id of the user. This is the user that updated the data. Remember that public
                           formulary also has the id of the user, so we have the 'is_public' to know that it is a public formulary.
            company_id (int): The Company instance id on what company does this formulary data was updated. 
            form_id (int): The Form instance id, on what formulary this data was updated. 
            form_data_id (int): What was the data updated. 
            is_public (bool): Is it a public formulary or not?
        """
        reflow_automation_service = ReflowAutomationService(company_id, user_id)
        reflow_automation_service.formulary_data_updated(form_id, form_data_id, data)