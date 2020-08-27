from django.contrib.auth.models import UserManager


class UserExtendedBillingManager(UserManager):
    def users_active_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id, is_active=True)

    def user_ids_active_by_company_id(self, company_id):
        return self.users_active_by_company_id(company_id).values_list('id', flat=True)