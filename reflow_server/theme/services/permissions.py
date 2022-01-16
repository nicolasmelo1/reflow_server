from reflow_server.formulary.services.permissions import FormularyPermissionsService
from reflow_server.theme.models import Theme, ThemeForm


class ThemePermissionService:
    """
    Used for validating the theme permissions.
    """
    @staticmethod
    def is_valid(user, company_id, theme_id):
        return Theme.theme_.exists_theme_by_theme_id_user_id_and_company_id(theme_id, user.id, company_id)

    @staticmethod
    def can_add_theme_based_on_number_of_pages_permission(company_id, theme_id):
        """
        Verifies if the user can add a theme based on the number of pages that the user has access to.

        Args:
            company_id (int): The company id that the user is from.
            theme_id (int): The theme id that the user is trying to add.

        Returns:
            bool: True if the user can add a theme based on the number of pages that the user has access to.
        """
        number_of_forms = ThemeForm.theme_.count_formularies_by_theme_id(theme_id)
        return FormularyPermissionsService.can_add_new_formulary(company_id, number_of_forms)