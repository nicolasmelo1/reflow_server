from django.db import transaction

from reflow_server.formulary.models import FieldOptions, OptionAccessedBy
from reflow_server.authentication.models import UserExtended


class FieldOptionsService:
    def __init__(self, user_id, company_id):
        self.company_id = company_id
        self.user_id = user_id

    @transaction.atomic
    def update_fields_options_accessed_by_user(self, field_option_ids):
        """
        This method is used to update the options the user have access to in the formularies.
        This filter is used so we can filter the data the user can access and the data the user cannot access.

        Args:
            field_option_ids (list(int)): A list of field_option_ids, this list are the field_option_ids the user has access to. 
                                          The ones that are not in this list are removed from the user.

        Returns:
            bool: returns True to show everything went fine.
        """
        OptionAccessedBy.objects.filter(user_id=self.user_id).exclude(field_option__in=field_option_ids).delete()
        already_existing_field_option_ids_the_user_can_access = OptionAccessedBy.objects.filter(
            user_id=self.user_id, 
            field_option__in=field_option_ids
        ).values_list('field_option_id', flat=True)
        for field_option_id in field_option_ids:
            if field_option_id not in already_existing_field_option_ids_the_user_can_access:
                OptionAccessedBy.objects.create(user_id=self.user_id, field_option_id=field_option_id)
                
        return True
    
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
        created_field_options=list()
        FieldOptions.objects.exclude(id__in=field_options_data.field_options_ids).filter(field=field).delete()
        for field_option_index, field_option_data in enumerate(field_options_data.field_options):
            option, created = FieldOptions.objects.update_or_create(
                id=field_option_data.field_option_id,
                field=field,
                defaults={
                    'option': field_option_data.option,
                    'order': field_option_index
                })
            if created:
                created_field_options.append(option)
        
        # when you create a new field option, all of the users have access to this option
        # automatically
        company_user_ids = UserExtended.formulary_.user_ids_active_by_company_id(self.company_id)

        OptionAccessedBy.objects.bulk_create([
            OptionAccessedBy(field_option=created_field_option, user_id=company_user_id)
            for created_field_option in created_field_options for company_user_id in company_user_ids
        ])
        return True

    def remove_field_options_from_field(self, field_id):
        FieldOptions.objects.filter(field_id=field_id).delete()
        return True
