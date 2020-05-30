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

    @staticmethod
    def change_password(temporary_password, password):
        """
        Changes the user password based on a jwt token recieved

        Arguments:
            temporary_password {str} -- temporary password, must be the jwt temporary password recieved
            password {str} -- The new user password
        """
        jwt = JWT(temporary_password)
        if UserExtended.objects.filter(temp_password=temporary_password).exists() and jwt.is_valid():
            user = UserExtended.objects.filter(id=jwt.data['id']).first()
            user.temp_password = None
            user.set_password(password)
            user.save()