from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.models import PublicAccessForm


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
            if int(formulary_id) in FormularyService(user_id, company_id).formulary_ids_the_user_has_access_to:
                return True
        elif formulary_name:
            if formulary_name in FormularyService(user_id, company_id).formulary_names_the_user_has_access_to:
                return True
        return False