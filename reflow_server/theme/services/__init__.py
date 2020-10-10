from .select import ThemeSelectService
from .update import ThemeUpdateService

from reflow_server.theme.models import ThemeField
from reflow_server.formulary.models import Field, FormAccessedBy


class ThemeService:
    @staticmethod
    def select_theme(theme_id, company_id, user_id):
        """
        Used when the user selects a theme, this copies the theme data and paste on the users table. This uses the
        ThemeSelectService for selecting templates

        Args:
            theme_id (int): A Theme instance is, what theme the user have selected
            company_id (int): A Company instance id, for what company the user has selected the template
            user_id (int): A UserExtended instance id, this is the user that has selected the template

        Returns:
            bool: returns True to indicate that everything was created
        """
        return ThemeSelectService(theme_id, company_id, user_id).select()

    @staticmethod
    def update_or_create_theme(theme_type_id, display_name, is_public, description, user_id, company_id, form_ids=[], theme_id=None):
        """
        Used for creating or updating templates. This uses the ThemeUpdateService to update or create templates

        Args:
            theme_type_id (int): this an existing reflow_server.theme.models.ThemeType instance id
            display_name (str): The name of your template, what you want to show
            is_public (bool): Public means users will be able to see the templates.
            description (str): A simple description of what the template do
            user_id (int): What user is creating this template, for some data we will use the data of this specific user.
            company_id (int): The company where the user is editing the templates
            form_ids (list(int), optional): This is only optional when editing themes, otherwise it is obligatory. It holds the main formulary ids to create
                                       templates from. Defaults to [].
            theme_id (int, optional): This is a Theme intance id, used only when editing an existing instance. Defaults to None.

        Returns:
            bool: return True to indicate everything went fine
        """
        return ThemeUpdateService().create_or_update(theme_type_id, display_name, is_public, description, user_id, company_id, form_ids, theme_id)

    @classmethod
    def get_forms_the_user_can_select(cls, company_id, user_id):
        """
        As the name of the method suggests gets the formularies list that the user can select to create templates. 
        What you need to know here is that if the user has access to a formulary but this formulary is connected
        to another that he does not have access, then he cannot use this formulary to create templates.

        Args:
            company_id (int): A Company instance id
            user_id (int): A UserExtended instance id

        Returns:
            list(int): A list of formularies ids the user can use to create templates.
        """
        dependent_form_ids = cls.get_dependent_formularies(company_id)
        form_ids_user_has_access_to = list(FormAccessedBy.theme_.formulary_ids_of_a_user_id(user_id))
        
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
        forms_dependency = Field.theme_.depends_on_id_and_form_field_as_option_depends_on_id_by_company_id(company_id)
        
        data = dict()
        for key_form_id, depends_on_form_id in forms_dependency:
            data[key_form_id] = data.get(key_form_id, []) + [depends_on_form_id]
        
        return data