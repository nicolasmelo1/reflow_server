from reflow_server.data.services import DataService


class DataPermissionsService:
    @staticmethod
    def is_valid(user_id, company_id, form_id, dynamic_form_id):
        data_service = DataService(user_id, company_id)
        form_data_ids = data_service.get_user_form_data_ids_from_form_id(form_id)
        if int(dynamic_form_id) in form_data_ids:
            return True
        else:
            return False