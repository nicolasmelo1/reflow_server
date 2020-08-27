from django.contrib.auth.models import UserManager


class UserExtendedAuthenticationManager(UserManager):
    def create_user(self, email, first_name, last_name, company_id, profile_id, phone=None, password=None):
        """
        Creates a new user in the database. This method uses the `create_user` method from the
        `UserManager` class. You will notice that password is default to None, this is because 
        that when we create the user we send an welcome e-mail for him to change the password.
        When the password is not set, we don't use the `create_user` method.

        Args:
            email (str): The email to set for this user, we use the email as the email and also as the username
                         of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user
            company_id (int): This is a Company instance id we always append an user to a specific company.
            profile_id (int): This is a Profiles instance id. This profile defines what the user can do on the company.
            phone (str, optional): Usually required only on onboarding. Defaults to None.
            password (str, optional): Not required because sometimes we just create the user without setting password. 
                                      Defaults to None.

        Returns:
            reflow_server.authentication.models.UserExtended: The newly created UserExtended instance.
        """
        if password:
            instance = super().create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                company_id=company_id,
                phone=phone,
                profile_id=profile_id
            )
        else:
            instance = self.create(
                username=email,
                email=email,
                first_name=first_name,
                last_name=last_name,
                company_id=company_id,
                phone=phone,
                profile_id=profile_id
            )
        return instance

    def update_user(self, user_id, email, first_name, last_name, profile_id, phone=None, password=None):
        """
        Updates a single user instance based on a user_id, gets the user instance using the `user_by_user_id` method
        and then updates the instance. Since phone and password are not required we just update them when they are
        NOT None.

        Args:
            user_id (int): A UserExtended instance id, this is the id of the user you want to update.
            email (str): Same as `create_user` method, the email is set on the `username` and `email` columns
            first_name (str): The first name of the User instance
            last_name (str): The last name of the User instance
            profile_id (int): The Profiles instance id to use for this user.
            phone (str, optional): The phone of the user as string. Defaults to None.
            password (str, optional): The password of the user. Defaults to None.

        Returns:
            reflow_server.authentication.models.UserExtended: The updated UserExtended instance.
        """
        instance = self.user_by_user_id(user_id)
        if instance:
            instance.username = email
            instance.email = email
            instance.first_name = first_name
            instance.last_name = last_name
            instance.profile_id = profile_id
            if phone:
                instance.phone = phone
            if password:
                instance.set_password(password)
            instance.save()

        return instance

    def create_temporary_password_for_user(self, email):
        """
        Creates a temporary password based on the user email. This temporary password is something we defined
        in the UserExtended class. This is just a jwt token with the data of the user.

        Args:
            email (str): The email of the user you want to create a temporary password

        Returns:
            tuple(reflow_server.authentication.models.UserExtended or None, str or None): Returns a tuple where the first element is
                                                                                          the instance or none and the second element
                                                                                          is the temporary_password as string or None
                                                                                          
        """
        instance = self.user_active_by_email(email)
        if instance:
            return instance, instance.make_temporary_password()
        return instance, None 

    def update_user_password(self, user_id, password):
        """
        Updates the password of a user given an user_id

        Args:
            user_id (int): An UserExtended instance id
            password (str): The new password to set for this user

        Returns:
            reflow_server.authentication.models.UserExtended: The updated UserExtended instance.
        """
        instance = self.user_by_user_id(user_id)
        if instance:
            instance.temp_password = None
            instance.set_password(password)
            instance.save()
        return instance
    
    def user_active_by_email(self, email):
        """
        Retrieves a user by email. This only filters for ACTIVE USERS.

        Args:
            email (str): The email you want to search

        Returns:
            reflow_server.authentication.models.UserExtended: The found UserExtended instance.
        """
        return self.get_queryset().filter(email=email, is_active=True).first()

    def user_active_by_user_id_and_company_id(self, user_id, company_id):
        """
        Retrieves a user by company_id and by its instance id. This only filters for ACTIVE USERS.

        Args:
            user_id (int): An UserExtended instance id
            company_id (int): An Company instance id that this user is from.

        Returns:
            reflow_server.authentication.models.UserExtended: The found UserExtended instance.
        """
        return self.get_queryset().filter(company_id=company_id, id=user_id, is_active=True).first()

    def user_by_user_id(self, user_id):
        """
        Retrieves a user by its id.

        Args:
            user_id (int): An UserExtended instance id

        Returns:
            reflow_server.authentication.models.UserExtended: The found UserExtended instance.
        """
        return self.get_queryset().filter(id=user_id).first()
    
    def users_active_by_company_id_ordered_by_descendinc_id(self, company_id):
        """
        Retrieves a queryset of ACTIVE UserExtended instances ordered by the bigger id to the lowest id.
        This filters by company_id.

        Args:
            company_id (int): An Company instance id that the users must be from.

        Returns:
            django.db.models.QuerySet(reflow_server.authentication.models.UserExtended): An queryset of ordered UserExtended instances
                                                                                         of the company selected
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True).order_by('-id')

    def exists_user_by_email(self, email):
        return self.get_queryset().filter(username=email).exists()

    def exists_user_by_email_excluding_id(self, email, user_id):
        return self.get_queryset().filter(username=email).exclude(id=user_id).exists()

    def exists_user_by_temporary_password(self, temporary_password):
        return self.get_queryset().filter(temp_password=temporary_password).exists()

    def remove_user_by_user_id_and_company_id(self, user_id, company_id):
        """
        Removes an ACTIVE user based on it's user_id and company_id.

        Args:
            user_id (int): An UserExtended instance id
            company_id (int): An Company instance id that this user is from.
        """
        return self.user_active_by_user_id_and_company_id(user_id, company_id).delete()