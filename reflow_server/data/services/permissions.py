from reflow_server.data.services import DataService


class DataPermissionsService:
    @staticmethod
    def is_valid(user_id, company_id, form_id, dynamic_form_id):
        """
        This function is used to validate if a user have access for the data of a formulary.
        We can filters on what each user can see and what each user cannot see. This is for this. 

        You might want to check reflow_server.data.services.DataService for further reference.

        Returns:
            bool: true if is valid, so everything can go as normal, and false if not valid, so the user don't have access to this data.
        """
        data_service = DataService(user_id, company_id)
        form_data_ids = data_service.get_user_form_data_ids_from_form_id(form_id)
        if int(dynamic_form_id) in form_data_ids:
            return True
        else:
            return False
