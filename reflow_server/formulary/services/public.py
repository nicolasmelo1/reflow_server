from reflow_server.formulary.models import PublicAccessForm, PublicAccessField
from reflow_server.authentication.services.public import PublicAccessService


class PublicFormularyService:
    @staticmethod
    def update_public_formulary(company_id, user_id, form_id, field_ids, greetings_message=None, description_message=None, is_to_submit_another_response_button=False):
        """
        Updates the public formulary, all of the fields defined here are publicly enabled, if a field is not publicly enabled
        we WILL NOT consider it when saving the formulary.
        
        Args:
            company_id (int): A Company instance id
            user_id (int): A UserExtended instance id, this is the user we will consider when saving the formulary. This means
                           an unauthenticated user will use the public api on behalf of this user.
            form_id (int): A form instance id. This is a MAIN FORM, this means this instance has depends_on as None
            field_ids (list(int)): List of Field instance ids. Those are the field to consider when saving the formulary.
            greetings_message (str, optional): A custom greetings message after the user filled the formulary. Defaults to None.
            description_message (str, optional): A custom description message to show at the top of the formulary, before the user fills
                                                 the form. Defaults to None.
            is_to_submit_another_response_button (bool, optional): Show a custom button to submit another response after the form
                                                                   has been filled. Defaults to False.

        Returns:
            str: The created or updated public key
        """
        public_access_instance = PublicAccessService(user_id, company_id).update()
        if len(field_ids) > 0:
            public_access_form_instance = PublicAccessForm.formulary_.update_or_create(
                public_access_instance.id, 
                form_id,
                greetings_message,
                description_message,
                is_to_submit_another_response_button
            )
            PublicAccessField.formulary_.bulk_create_and_delete(
                public_access_instance.public_key,
                public_access_instance.id,
                public_access_form_instance.id,
                field_ids
            )
        else:
            PublicAccessForm.formulary_.delete_by_public_access_key_and_main_form_id(public_access_instance.public_key, form_id)
        return public_access_instance.public_key