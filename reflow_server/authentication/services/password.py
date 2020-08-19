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
        user = UserExtended.objects.filter(username=email).first()
        if user:
            temp_password = user.make_temporary_password()
            url = change_password_url.replace(r'{}', temp_password)
            NotifyService.notify_forgot_password(user, temp_password, url)

    def isvalid_temporary_password(self, temporary_password):
        """
        Validates if a temporary password is valid before changing the old password to the new password

        Arguments:
            temporary_password {str} -- temporary password, must be the jwt temporary password recieved

        Returns:
            bool -- True or false depending if it is valid or not.
        """
        self.jwt = JWT(temporary_password)
        return UserExtended.objects.filter(temp_password=temporary_password).exists() and self.jwt.is_valid()

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
        user = UserExtended.objects.filter(id=self.jwt.data['id']).first()
        user.temp_password = None
        user.set_password(new_password)
        user.save()