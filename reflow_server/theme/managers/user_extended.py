from django.contrib.auth.models import UserManager


class UserExtendedThemeManager(UserManager):
    def users_active_by_company_id(self, company_id):
        """
        Gets the active users of a company. This gets a Queryset of
        UserExtended instances.

        Args:
            company_id (int): This is a Company instance id to filter the users

        Returns:
            django.db.models.QuerySet(reflow_server.authentication.models.UserExtended): 
            A queryset of active UserExtended instances.
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True)
