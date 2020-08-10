from reflow_server.formulary.services.formulary import FormularyService


class FormularyPermissionsService:
    @staticmethod
    def is_valid_form(user_id, company_id, formulary_id):
        if int(formulary_id) in FormularyService(user_id, company_id).formulary_ids_the_user_has_access_to:
            return True
        else:
            return False