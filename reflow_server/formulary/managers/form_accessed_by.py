from django.db import models


class FormAccessedByFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def main_forms_accessed_by_user_id_and_enabled_ordered_by_order(self, user_id):
        """
        Gets the FormAccessedBy instances ordered by order from a single user_id.

        Args:
            user_id (int): A UserExtended instance id.

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.FormAccessedBy): A queryset of FormAccessedBy instances ordered
            by order of enabled forms and that are the main forms.
        """
        return self.get_queryset().filter(user_id=user_id, form__enabled=True, form__depends_on__isnull=True).order_by('form__order')

    def main_form_names_accessed_by_user_id_and_enabled_ordered_by_order(self, user_id):
        """
        Gets a list of Form form_name's. This is used so we can know the names of the formularies the user has access to.

        Args:
            user_id (int): A UserExtended instance id.

        Returns:
            django.db.models.QuerySet(str): A queryset of form_names, those names works like ids (unique for each company) for formularies,
            but instead of displaying the name, we display 
        """
        return self.main_forms_accessed_by_user_id_and_enabled_ordered_by_order(user_id).values_list('form__form_name', flat=True)

    def main_form_ids_accessed_by_user_id_and_enabled_ordered_by_order(self, user_id):
        """
        Gets a list of Form id's. This is used so we can know the id of the formularies the user has access to.

        Args:
            user_id (int): A UserExtended instance id.

        Returns:
            django.db.models.QuerySet(int): A queryset of Form instance ids
        """
        return self.main_forms_accessed_by_user_id_and_enabled_ordered_by_order(user_id).values_list('form_id', flat=True)