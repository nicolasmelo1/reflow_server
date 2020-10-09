from reflow_server.theme.models import Theme


class ThemePermissionService:
    """
    Used for validating the theme permissions.
    """
    @staticmethod
    def is_valid(user, company_id, theme_id):
        return Theme.theme_.exists_theme_by_theme_id_user_id_and_company_id(theme_id, user.id, company_id)
