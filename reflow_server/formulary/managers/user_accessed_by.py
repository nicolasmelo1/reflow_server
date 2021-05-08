from django.db import models

class UserAccessedByFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_or_update(self, field_id, user_id, user_option_id):
        """
        Updates or creates a UserAccessedBy instance

        Args:
            field_id (int): A Field instance id
            user_id (int): A UserExtended instance id, this user_id is the user for wwho this filter refers to
            user_option_id (int): A UserExtended instance id, this is the user_option_id, which is the option 
            that the user can access

        Returns:
            reflow_server.formulary.models.UserAccessedBy: The created or updated UserAccessedBy instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            user_id=user_id,
            field_id=field_id,
            user_option_id=user_option_id
        )

        return instance
    
    def users_accessed_by_by_field_id_company_id_and_user_id(self, field_id, company_id, user_id):
        return self.get_queryset().filter(
            field_id=field_id, 
            field__form__depends_on__group__company_id=company_id, 
            user_id=user_id
        )