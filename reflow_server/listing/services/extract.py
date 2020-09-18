from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.listing.models import ListingSelectedFields, ExtractFileData
from reflow_server.formulary.models import Form
from reflow_server.data.services import DataService

from datetime import datetime
import uuid


class ExtractService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
        
    def is_valid_data(self, from_date, to_date, sort_value=[], sort_field=[], 
                      search_value=[], search_field=[], search_exact=[]):

        if sort_value or sort_field:
            # if there is not both
            if not sort_value and sort_field:
                return False
            if len(sort_value) != len(sort_field):
                return False

        if search_value or search_field or search_exact:
            # if there is not all
            if not search_value and search_field and search_exact:
                return False
            # if any of the 3 does not have equal lengths
            if any(len(lst) != len(search_field) for lst in [search_value, search_exact]):
                return False
        return True

    def __start_extraction(self, file_id, user_id, company_id, form_id, 
                           file_format, from_date, to_date, 
                           fields_ids, sort_value=[], sort_field=[], 
                           search_value=[], search_field=[], search_exact=[]):

        data_service = DataService(user_id, company_id)

        to_date = DataService.validate_and_extract_date_from_string(to_date)
        from_date = DataService.validate_and_extract_date_from_string(from_date)
        # get correct data to pass as parameters
        converted_search_data = data_service.convert_search_query_parameters(search_field, search_value, search_exact)
        converted_sort_data = data_service.convert_sort_query_parameters(sort_field, sort_value)

        form_data_accessed_by_user = data_service.get_user_form_data_ids_from_form_id(form_id, converted_search_data, converted_sort_data, from_date, to_date)
        # call external service
        from reflow_server.listing.externals import ExtractDataWorkerExternal
        response = ExtractDataWorkerExternal().build_extraction_data(file_id, file_format, company_id, user_id, form_id, fields_ids, form_data_accessed_by_user)
        print('BREAKPOINT')
        print(response.content)

    def extract(self, file_format, from_date, to_date, 
                sort_value=[], sort_field=[], 
                search_value=[], search_field=[], search_exact=[]):
        file_id = uuid.uuid4()
        while ExtractFileData.objects.filter(file_id=file_id).exists():
            file_id = uuid.uuid4()
        file_id = str(file_id)
        form = Form.objects.filter(
            form_name=self.form_name,
            group__company_id=self.company_id,
            depends_on__isnull=True
        ).first()
        user_listing_selected_fields_for_form = ListingSelectedFields.objects.filter(
            is_selected=True,
            user_id=self.user_id, 
            field__form__depends_on__group__company_id=self.company_id, 
            field__form__depends_on__form_name=self.form_name
        ).order_by('field__form__order', 'field__order')

        fields_ids = []
        for user_listing_selected_field_for_form in user_listing_selected_fields_for_form:
            fields_ids.append(str(user_listing_selected_field_for_form.field.id))
              
        async_task = RunAsyncFunction(self.__start_extraction)
        async_task.delay(file_id=file_id, user_id=self.user_id, company_id=self.company_id, form_id=form.id, 
                         file_format=file_format, from_date=from_date, to_date=to_date, fields_ids=fields_ids,
                         sort_value=sort_value, sort_field=sort_field, 
                         search_value=search_value, search_field=search_field, search_exact=search_exact)
        return file_id