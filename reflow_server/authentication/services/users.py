from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.authentication.models import UserExtended, Company, VisualizationType
from reflow_server.billing.services import BillingService
from reflow_server.formulary.models import UserAccessedBy, Field
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.notify.services import NotifyService
from reflow_server.kanban.services import KanbanService

from datetime import datetime


class UsersService:
    def __init__(self, company_id, user_id):
        self.company = Company.authentication_.company_by_company_id(company_id)
        self.user_id = user_id
    
    @staticmethod
    def is_self(user_id, request_user_id):
        """
        This is used to check if the user that is being edited is itself or not. The user cannot update itself.
        This method is kinda dumb if you think about it. But it exposes a business rule that a user
        cannot edit itself.
        """
        return request_user_id == user_id

    def remove_user(self):
        """
        When we remove a user we just need to update the billing information
        """
        BillingService(self.company.id, self.user_id).update_charge()

    @transaction.atomic
    def create(self, email, first_name, last_name, profile, field_option_ids_accessed_by, form_ids_accessed_by, users_accessed_by, change_password_url):
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
            users_accessed_by (list(reflow_server.authentication.services.data.UserAccessedByData)): A list of UserAccessedByData objects so we can change the users
                                                                                                     the user can access for a certain field.
            change_password_url (str): The url to change the password of the user.

        Returns:
            reflow_server.authentication.models.UserExtended: the instance of the created user.
        """
        visualization_type_id = VisualizationType.objects.filter(name='listing').values_list('id', flat=True).first()

        instance = UserExtended.authentication_.create_user(
            email,
            first_name,
            last_name,
            self.company.id,
            profile.id,
            visualization_type_id
        )

        self.__update_user_formularies_and_options_permissions(instance.id, form_ids_accessed_by, field_option_ids_accessed_by)
        self.__create_new_user_notify_update_billing_and_add_kanban_defaults(instance, change_password_url)
        self.__update_user_users_permission(instance.id, users_accessed_by)
        self.__create_user_user_pemissions_when_user_is_created(instance.id)
        return instance

    @transaction.atomic
    def update(self, user_id, email, first_name, last_name, profile, field_option_ids_accessed_by, form_ids_accessed_by, users_accessed_by):
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
            users_accessed_by (list(reflow_server.authentication.services.data.UserAccessedByData)): A list of UserAccessedByData objects so we can change the users
                                                                                                     the user can access for a certain field.
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
            self.__update_user_users_permission(instance.id, users_accessed_by)
        return instance

    def __create_user_user_pemissions_when_user_is_created(self, created_user_id):
        users_from_company = UserExtended.authentication_.users_active_by_company_id(self.company.id)
        users_fields = Field.objects.filter(form__depends_on__group__company_id=self.company.id, type__type='user')
        for field in users_fields:
            for user in users_from_company:
                UserAccessedBy.objects.update_or_create(
                    user=user,
                    field=field,
                    user_option_id=created_user_id
                )

    def __create_new_user_notify_update_billing_and_add_kanban_defaults(self, instance, change_password_url):
        """
        This function notifies a new user with an email with his new password but also creates the billing information of this user.
        This also sets the kanban defaults for the user, this means we cop the kanban_defaults of a user and passes it to the newly created
        user.
        
        Args:
            instance (reflow_server.authentication.models.UserExtended): The newly created instance of the user
            change_password_url (str): The url to change the password

        Returns:
            bool: Return True to set that everything went fine.
        """
        password = instance.make_temporary_password()

        BillingService(self.company.id, self.user_id).update_charge()
        NotifyService.send_welcome_mail(instance.email, password, self.company.name, change_password_url.replace(r'{}', password))
        KanbanService.copy_defaults_to_company_user(self.company.id, self.user_id, instance.id)
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
        FieldOptionsService(self.company.id).update_fields_options_accessed_by_user(user_id, field_option_ids_accessed_by)

        return True

    def __update_user_users_permission(self, user_id, users_accessed_by):
        """
        Updates the user permissions, similar from filtering the data by the options we can filter the data by the user options
        so let's for example imagine the following scenario: We have 'Lucas' and 'Nicolas' users. 

        'Lucas' can only see what is from Lucas and 'Nicolas' can only see what is from Nicolas. With this functionality we can filter
        what the user can see.

        But let's imagine the following scenario: 
        The formulary has two user fields: 'Who created' and 'Responsible for Task'.

        Who created can be anyone but the Responsible for Task should be only for the specific user.
        In this scenario we filter just by the `Responsible for Task` value

        Args:
            user_id (int): A UserExtended instance id, this is the id of the user you are creating or updating
            users_accessed_by (reflow_server.authentication.services.data.UserAccessedByData): A class responsible for holding the user accessed by options
        """
        saved_instances_ids = []
        for user_accessed_by in users_accessed_by:
            instance, __ = UserAccessedBy.objects.update_or_create(
                user_id=user_id,
                field_id=user_accessed_by.field_id,
                user_option_id=user_accessed_by.user_id
            )
            saved_instances_ids.append(instance.id)

        UserAccessedBy.objects.filter(user_id=user_id).exclude(id__in=saved_instances_ids).delete()

    @staticmethod
    def update_refresh_token_and_user_last_login(self, user):
        """
        When the refresh token is updated we interpret it as the user made login in our platform
        because the user can stay logged in forever in our platform without the need of making login
        again.

        Args:
            user (reflow_server.authentication.models.UserExtended): The UserExtended instance that we 
                                                                     need to update.

        Returns:
            reflow_server.authentication.models.UserExtended: The UserExtended instance updated.
        """
        user.last_login = datetime.now()
        Event.register_event('user_refresh_token', {
            'company_id': user.company_id,
            'user_id': user.id
        })
        user.save()
        return user