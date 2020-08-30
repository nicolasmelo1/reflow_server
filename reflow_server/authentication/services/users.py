from django.db import transaction

from reflow_server.authentication.models import UserExtended, Company
from reflow_server.billing.services import BillingService
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.notify.services import NotifyService

class UsersService:
    def __init__(self, company_id):
        self.company = Company.authentication_.company_by_company_id(company_id)
    
    @staticmethod
    def is_self(user_id, request_user_id):
        """
        This is used to check if the user that is being edited is itself or not. The user cannot update itself.
        """
        return request_user_id == user_id

    def remove_user(self):
        """
        When we remove a user we just need to update the billing information, actually, just the payment gateway
        """
        BillingService(self.company.id).charge_service.push_updates()

    @transaction.atomic
    def create(self, email, first_name, last_name, profile, field_option_ids_accessed_by, form_ids_accessed_by, change_password_url):
        """
        Creates a new user with it's permissions. When we create a new user we also create the billing

        Args:
            email (str): The email of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user, the name of the user must contain the first and the last name.
            profile (reflow_server.authentication.models.Profiles): this is an `reflow_server.authentication.models.Profiles` model.
            field_option_ids_accessed_by (list(int)): The integers in this list are ids of formularies the user has access to. The ones that
                                                      are not in this list are removed from the user. So if the user has access to the form_id 23
                                                      but this list is [24,25] the user will have access to form_ids 24 and 25 and will lose the access
                                                      on form_id 23.
            form_ids_accessed_by (list(int)): The integers in this list are ids of field options the user has access to. It works the same as `field_option_ids_accessed_by`
                                              parameter. The ones that are not in this list are removed from the user.
            change_password_url (str): The url to change the password of the user.

        Returns:
            reflow_server.authentication.models.UserExtended: the instance of the created user.
        """
        instance = UserExtended.authentication_.create_user(
            email,
            first_name,
            last_name,
            self.company.id,
            profile.id
        )

        self.__update_user_formularies_and_options_permissions(instance.id, form_ids_accessed_by, field_option_ids_accessed_by)
        self.__create_new_user_notify_and_update_billing(instance, change_password_url)
    
        return instance

    @transaction.atomic
    def update(self, user_id, email, first_name, last_name, profile, field_option_ids_accessed_by, form_ids_accessed_by):
        """
        Updates a user and it's permissions to both formularies and options.

        Args:
            user_id (int): The id of the user you are updating
            email (str): The email of the user
            first_name (str): The first name of the user
            last_name (str): The last name of the user, the name of the user must contain the first and the last name.
            profile (reflow_server.authentication.models.Profiles): this is an `reflow_server.authentication.models.Profiles` model.
            field_option_ids_accessed_by (list(int)): The integers in this list are ids of formularies the user has access to. The ones that
                                                      are not in this list are removed from the user. So if the user has access to the form_id 23
                                                      but this list is [24,25] the user will have access to form_ids 24 and 25 and will lose the access
                                                      on form_id 23.
            form_ids_accessed_by (list(int)): The integers in this list are ids of field options the user has access to. It works the same as `field_option_ids_accessed_by`
                                              parameter. The ones that are not in this list are removed from the user.

        Returns:
            reflow_server.authentication.models.UserExtended: the instance of the updated user.
        """
        instance = UserExtended.authentication_.update_user(
            user_id,
            email,
            first_name,
            last_name,
            profile.id
        )
        
        if instance:
            self.__update_user_formularies_and_options_permissions(instance.id, form_ids_accessed_by, field_option_ids_accessed_by)

        return instance

    def __create_new_user_notify_and_update_billing(self, instance, change_password_url):
        """
        This function notifies a new user with an email with his new password but also creates the billing information. Of this user.

        Args:
            instance (reflow_server.authentication.models.UserExtended): The newly created instance of the user
            change_password_url (str): The url to change the password

        Returns:
            bool: Return True to set that everything went fine.
        """
        password = instance.make_temporary_password()

        BillingService(self.company.id).create_user(user_id=instance.id)
        NotifyService.send_welcome_mail(instance.email, password, self.company.name, change_password_url.replace(r'{}', password))

        return True

    def __update_user_formularies_and_options_permissions(self, user_id, form_ids_accessed_by, field_option_ids_accessed_by):
        """
        Updates a user permissions to both formularies and options.

        Args:
            user_id (int): The id of the user you want to update the permissions.
            field_option_ids_accessed_by (list(int)): The integers in this list are ids of formularies the user has access to. The ones that
                                                      are not in this list are removed from the user. So if the user has access to the form_id 23
                                                      but this list is [24,25] the user will have access to form_ids 24 and 25 and will lose the access
                                                      on form_id 23.
            form_ids_accessed_by (list(int)): The integers in this list are ids of field options the user has access to. It works the same as `field_option_ids_accessed_by`
                                              parameter. The ones that are not in this list are removed from the user.

        Returns:
            bool: returns True to show everything went fine
        """
        FormularyService(user_id, self.company.id).update_formulary_ids_the_user_has_access_to(form_ids_accessed_by)
        FieldOptionsService(user_id, self.company.id).update_fields_options_accessed_by_user(field_option_ids_accessed_by)

        return True