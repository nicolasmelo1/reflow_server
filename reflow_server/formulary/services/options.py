from django.db import transaction

from reflow_server.formulary.models import FieldOptions, OptionAccessedBy, Field
from reflow_server.authentication.models import UserExtended

import uuid


class FieldOptionsService:
    def __init__(self, company_id):
        self.company_id = company_id

    def update_all_at_once_field_options_accessed_by_user(self, user_id, field_option_ids):
        """
        Updates all of the field options that a user have access to at once, this is useful when editing or adding a new user

        Args:
            user_id (int): A UserExtended intance id. This is the id of the user you are inserting.
            field_option_ids (list(int)): A list of FieldOption instance ids
        """
        for field_id in Field.objects.filter(form__depends_on__group__company_id=self.company.id, type__type__in=['option', 'multi_option']).values_list('id', flat=True):
            self.update_fields_options_accessed_by_user(user_id, field_id, field_option_ids)

    @transaction.atomic
    def update_fields_options_accessed_by_user(self, user_id, field_id, field_option_ids):
        """
        This method is used to update the options the user have access to in the formularies.
        This filter is used so we can filter the data the user can access and the data the user cannot access.

        Args:
            field_option_ids (list(int)): A list of field_option_ids, this list are the field_option_ids the user has access to. 
                                          The ones that are not in this list are removed from the user.

        Returns:
            bool: returns True to show everything went fine.
        """
        OptionAccessedBy.objects.filter(user_id=user_id, field_option__field_id=field_id).exclude(field_option__in=field_option_ids).delete()
        already_existing_field_option_ids_the_user_can_access = OptionAccessedBy.objects.filter(
            user_id=user_id, 
            field_option__in=field_option_ids
        ).values_list('field_option_id', flat=True)
        for field_option_id in field_option_ids:
            if field_option_id not in already_existing_field_option_ids_the_user_can_access:
                OptionAccessedBy.objects.create(user_id=user_id, field_option_id=field_option_id)
    
    def create_new_field_options(self, field, field_options_data):
        """
        Creates new field_options for a specific field

        Args:
            field (reflow_server.formulary.models.Field): A field instance to create
            the options for.
            field_options_data (reflow_server.formulary.services.data.FieldOptionsData): A class used to
            hold all of the field options so we don't need to use serializers

        Returns:
            bool: returns True to indicate everything went fine.
        """
        created_or_updated_field_option_ids=list()
        FieldOptions.objects.exclude(uuid__in=[uuid.UUID(field_option_uuid) for field_option_uuid in field_options_data.field_options_uuids]).filter(field=field).delete()
        for field_option_index, field_option_data in enumerate(field_options_data.field_options):
            option, __ = FieldOptions.objects.update_or_create(
                uuid=field_option_data.field_option_uuid,
                field=field,
                defaults={
                    'option': field_option_data.option,
                    'order': field_option_index
                })
            created_or_updated_field_option_ids.append(option.id)
        
        # when you create a new field option, all of the users have access to this option
        # automatically
        company_user_ids = UserExtended.formulary_.user_ids_active_by_company_id(self.company_id)

        for user_id in company_user_ids:
            self.update_fields_options_accessed_by_user(user_id, field.id, created_or_updated_field_option_ids)
    
        return True

    def remove_field_options_from_field(self, field_id):
        FieldOptions.objects.filter(field_id=field_id).delete()
        return True
