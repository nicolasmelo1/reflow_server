from reflow_server.formulary.services.data.sort import DataSort
from reflow_server.formulary.services.data.search import DataSearch
from reflow_server.formulary.models import FormValue, OptionAccessedBy, DynamicForm, Field, FieldOptions, FormAccessedBy
from reflow_server.authentication.models import UserExtended

class DataService(DataSort, DataSearch):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
 
    def get_user_data_from_form(self, form_id, search_keys=None, sort_keys=None, from_date=None, to_date=None):
        """
        Retrieves the forms that a user has access to, it is a handy function also used for pagination, filtering and some tweeks of
        the forms that is retrieves
        :param form: str - the form name usually recieved as the parameter from the url
        :param search_keys: list of dicts - must be on the following format:
            {
                field_name: (value_to_search, 0 or 1)
            }
        :param sort_keys: list of dicts - must be on the following format:
            {
                field_name: value_to_sort
            }
        :param pagination: int - current page you want to retrieve data from.
        :param pagination_number: total number of data you want to retrieve per page.
        :param from_date: - datetime - the first datetime in the range when the form was updated
        :param to_date: - datetime - the last datetime in the range when the datetime the form was updated
        :return tuple containing the total number of forms used primarly for pagination and a queryset of DynamicForms
        """
        self.__fields = Field.objects.filter(
            form__company_id=self.company_id,
            form__depends_on_id=form_id
        ).values('id', 'name', 'type__type', 'form_field_as_option')

        # fields become a dict with each name becoming each key of the dict.
        self.__fields = {
            field['name']: {
                'id': field['id'],
                'type': field['type__type'],
                'form_field_as_option_id': field['form_field_as_option']
            } for field in self.__fields
        }

        if from_date and to_date:
            self.__data = DynamicForm.objects.filter(
                company_id=self.company_id, 
                updated_at__range=[from_date, to_date],
                form_id=form_id
            ).order_by('-updated_at')

        else:
            self.__data = DynamicForm.objects.filter(
                company_id=self.company_id, 
                form_id=form_id
            ).order_by('-updated_at')

        if search_keys:
            self.__search(search_keys)

        if sort_keys:
            self.__sort(sort_keys)

        self.__filter_by_profile_permissions(form_id)
        return self.__data

    def __filter_by_profile_permissions(self, form_id):
        user = UserExtended.objects.filter(id=self.user_id)
        if user.profile.name == 'simple_user':
            main_forms = self.__data.filter(user=self.user)
        else:
            options_accessed_by_user = OptionAccessedBy.objects.filter(
                user=self.user,
                field_option__field__form__depends_on_id=form_id
            ).values('field_option__field_id', 'field_option__option')

            if not options_accessed_by_user:
                # If there is no filter on this form_id, we return all the data to the user, like if he was an admin.
                return
            else:
                field_options_by_field = dict()
                options_by_field = dict()

                field_options = FieldOptions.objects.filter(
                    field__form__depends_on__group__company=self.company,
                    field__form__depends_on_id=form_id
                ).values('field_id', 'option')

                for option in options_accessed_by_user:
                    options_by_field[option['field_option__field_id']] = options_by_field.get(
                        option['field_option__field_id'], []
                    ) + [option['field_option__option']]

                for field_option in field_options:
                    field_options_by_field[field_option['field_id']] = field_options_by_field.get(
                        field_option['field_id'], []
                    ) + [field_option['option']]


                all_form_values = FormValue.objects.filter(
                    form__depends_on__in=self.__data,
                    field__in=list(options_by_field.keys()),
                    field_type__type__in=['option', 'multi_option'],
                    company_id=self.company_id
                ).order_by('form__depends_on')

                forms_to_ignore = list()
                for (value, field_id, field_type, form_depends_on) in all_form_values.values_list('value', 'field_id', 'field__type__type', 'form__depends_on'):
                    if field_id in options_by_field and value not in options_by_field[field_id]+[''] and field_id in field_options_by_field and value in field_options_by_field[field_id]:
                        forms_to_ignore.append(form_depends_on)
                self.__data.exclude(id__in=forms_to_ignore)


    
