from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.models import Form
from reflow_server.billing.models import CurrentCompanyCharge


class FormularyPermissionsService:
    @staticmethod
    def is_valid_form(user_id, company_id, formulary_id=None, formulary_name=None):
        """
        Checks if the user can access a particular formulary_id.

        Args:
            user_id (int): An UserExtended instance id
            company_id (int): An Company instance id that this user is from.
            formulary_id (int): A Form instance id, if the user does not have access for this formulary_id
            then te user cannot access or edit it's contents. Default to None.
            formulary_name (str): The name of the formulary to check if the user has access to. Default to None.
        Returns:
            bool: True id the user can access this formulary_id or False if not.
        """
        if formulary_id:
            if int(formulary_id) in FormularyService(user_id, company_id).formulary_ids_the_user_has_access_to_that_are_enabled:
                return True
        elif formulary_name:
            if formulary_name in FormularyService(user_id, company_id).formulary_names_the_user_has_access_to:
                return True
        return False

    @staticmethod
    def can_add_new_formulary(company_id, number_of_forms_being_added=1):
        """
        Checks if the user can create a new formulary in the company.

        Args:
            company_id (int): An Company instance id that this user is from.
            number_of_forms_being_added (int): The number of forms that the user is trying to create.

        Returns:
            bool: True id the user can create a new formulary in the company or False if not.
        """
        quantity_permission = CurrentCompanyCharge.formulary_.quantity_of_per_page_permission_for_company_id(company_id)
        actual_quantity = Form.formulary_.count_main_forms_by_company_id(company_id)
        if quantity_permission >= actual_quantity + number_of_forms_being_added:
            return True
        return False