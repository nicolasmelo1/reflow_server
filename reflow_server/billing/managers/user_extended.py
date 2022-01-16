from django.contrib.auth.models import UserManager


class UserExtendedBillingManager(UserManager):
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

    def user_ids_active_by_company_id(self, company_id):
        """
        Similar to `users_active_by_company_id` but get only the ids.

        Args:
            company_id (int): This is a Company instance id to filter the users

        Returns:
            django.db.models.QuerySet(int): Each integer is a UserExtended instance id.
        """
        return self.users_active_by_company_id(company_id).values_list('id', flat=True)

    def deactivate_all_accounts_except_oldest_by_company_id(self, company_id):
        user_id_to_ignore = self.get_queryset().filter(company_id=company_id).order_by('-date_joined').values_list('id', flat=True).first()
        return self.get_queryset().filter(company_id=company_id).exclude(id=user_id_to_ignore).update(is_active=False)

    def reactivate_all_accounts_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id).update(is_active=True)
