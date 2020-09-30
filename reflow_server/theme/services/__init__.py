from .select import ThemeSelectService

from reflow_server.theme.models import ThemeField
from reflow_server.formulary.models import Field


class ThemeService:
    @staticmethod
    def select_theme(theme_id, company_id, user_id):
        return ThemeSelectService(theme_id, company_id, user_id).select()

    
    @staticmethod
    def get_dependent_formularies(company_id):
        forms_dependency = Field.objects.filter(form__depends_on__group__company_id=company_id).exclude(form_field_as_option__isnull=True)\
                           .values_list('form__depends_on_id', 'form_field_as_option__form__depends_on_id')
        
        data = dict()
        for key_form_id, depends_on_form_id in forms_dependency:
            data[key_form_id] = data.get(key_form_id, []) + [depends_on_form_id]
        
        return data