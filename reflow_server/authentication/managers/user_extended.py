from django.contrib.auth.models import UserManager


class UserExtendedAuthenticationManager(UserManager):
    def user_active_by_email(self, email):
        return self.get_queryset().filter(email=email, is_active=True).first()

    def user_by_user_id(self, user_id):
        return self.get_queryset().filter(id=user_id).first()
