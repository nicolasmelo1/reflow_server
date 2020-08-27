from reflow_server.notify.services import NotifyService
from reflow_server.authentication.models import UserExtended
from reflow_server.authentication.utils.jwt_auth import JWT


class PasswordService:
    @staticmethod
    def request_new_temporary_password_for_user(email, change_password_url):
        """
        Requests a new temporary password for the user, if the user email exists, sends a email notification      

        Arguments:
            email {str} -- the email of the user
            change_password_url {str(url)} -- the url we will redirect two when the user 
                                              clicks the button to access the system
        """
        # search on username column instead of email column, username is always unique
        user, temporary_password = UserExtended.authentication_.create_temporary_password_for_user(email)
        if user:
            url = change_password_url.replace(r'{}', temporary_password)
            NotifyService.send_change_password(user.email, user.first_name, temporary_password, url)

    def isvalid_temporary_password(self, temporary_password):
        """
        Validates if a temporary password is valid before changing the old password to the new password

        Arguments:
            temporary_password {str} -- temporary password, must be the jwt temporary password recieved

        Returns:
            bool -- True or false depending if it is valid or not.
        """
        self.jwt = JWT(temporary_password)
        return UserExtended.authentication_.exists_user_by_temporary_password(temporary_password) and self.jwt.is_valid()

    def change_password(self, new_password):
        """
        Changes the user password based on a jwt token recieved

        Arguments:
            temporary_password {str} -- temporary password, must be the jwt temporary password recieved
            password {str} -- The new user password
        """
        if not hasattr(self, 'jwt'):
            raise AssertionError('Call `.isvalid_temporary_password()` to validate your temporary password and \n'
                                 'after calling `.change_password()` method.')
        user = UserExtended.authentication_.update_user_password(self.jwt.data['id'], new_password)
        return user