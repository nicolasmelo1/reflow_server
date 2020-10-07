from .select import ThemeSelectService
from .update import ThemeUpdateService

from reflow_server.theme.models import ThemeField
from reflow_server.formulary.models import Field, FormAccessedBy


class ThemeService:
    @staticmethod
    def select_theme(theme_id, company_id, user_id):
        return ThemeSelectService(theme_id, company_id, user_id).select()

    @staticmethod
    def update_or_create_theme(theme_type_id, display_name, is_public, description, user_id, company_id, form_ids=[], theme_id=None):
        return ThemeUpdateService().create_or_update(theme_type_id, display_name, is_public, description, user_id, company_id, form_ids, theme_id)

    @classmethod
    def get_forms_the_user_can_select(cls, company_id, user_id):
        dependent_form_ids = cls.get_dependent_formularies(company_id)
        form_ids_user_has_access_to = list(FormAccessedBy.objects.filter(user_id=user_id).values_list('form_id', flat=True))
        
        for dependent_form_id, depends_on_form_ids in dependent_form_ids.items():
            if dependent_form_id in form_ids_user_has_access_to:
                if any([depends_on_form_id not in form_ids_user_has_access_to for depends_on_form_id in depends_on_form_ids]):
                    form_ids_user_has_access_to.remove(dependent_form_id)
            
        return form_ids_user_has_access_to


    @staticmethod
    def get_dependent_formularies(company_id):
        """
        Gets the formularies ids that depends on others. Returns a dict with each key being a dependent formulary
        and the values is a list of formulary ids it depends on.

        This might be confused with depends_on on Form. But it's not this. This dependent formularies are main forms
        that have `form` field types. These field types are usually connected to another formulary. We use this because
        when creating themes, if we select a formulary that depends on other, we actually need to select it's dependencies.

        Args:
            company_id (int): The Company intance id that is creating a new theme.

        Returns:
            dict: Returns a dict with each key being a dependent formulary
                  and the values is a list of formulary ids it depends on.
        """
        forms_dependency = Field.objects.filter(form__depends_on__group__company_id=company_id).exclude(form_field_as_option__isnull=True)\
                           .values_list('form__depends_on_id', 'form_field_as_option__form__depends_on_id')
        
        data = dict()
        for key_form_id, depends_on_form_id in forms_dependency:
            data[key_form_id] = data.get(key_form_id, []) + [depends_on_form_id]
        
        return data