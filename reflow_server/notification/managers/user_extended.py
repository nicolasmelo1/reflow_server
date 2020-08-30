from django.contrib.auth.models import UserManager


class UserExtendedNotificationManager(UserManager):
    def user_by_user_id(self, user_id):
        """
        Retrieves a user by its id.

        Args:
            user_id (int): An UserExtended instance id

        Returns:
            reflow_server.authentication.models.UserExtended: The found UserExtended instance.
        """
        return self.get_queryset().filter(id=user_id).first()
    
    def user_ids_active_by_company_id(self, company_id):
        """
        Gets the active user ids of a company.

        Args:
            company_id (int): This is a Company instance id to filter the users

        Returns:
            django.db.models.QuerySet(int): Each integer is a UserExtended instance id.
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True).values_list('id', flat=True)

    def exists_user_id_excluding_admin(self, user_id):
        return self.get_queryset().filter(id=user_id).exclude(profile__name='admin').exists()