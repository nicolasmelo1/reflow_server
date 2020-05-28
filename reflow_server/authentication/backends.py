from reflow_server.authentication.models import UserExtended


class EmailBackend:
    """
    With this, the user logs in using email and password as default, not by
    username and password.
    """
    def authenticate(self, request,  username=None, password=None):
        user = UserExtended.objects.filter(email=username, is_active=True).first()
        if user and user.check_password(password):
            return user
        else:
            return None
        return None

    def get_user(self, user_id):
        try:
            return UserExtended.objects.get(id=user_id)
        except UserExtended.DoesNotExist:
            return None
