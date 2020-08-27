from reflow_server.authentication.models import UserExtended


class EmailBackend:
    """
    With this, the user logs in using email and password as default, not by
    username and password.
    """
    def authenticate(self, request,  username=None, password=None):
        user = UserExtended.authentication_.user_active_by_email(username)        
        if user and user.check_password(password):
            return user
        else:
            return None
        return None

    def get_user(self, user_id):
        return UserExtended.authentication_.user_by_user_id(user_id)
