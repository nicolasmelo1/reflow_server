from django.db import models


class FormAccessedByThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def formulary_ids_of_a_user_id(self, user_id):
        """
        Returns the formulary ids a user has access to

        Args:
            user_id (int): The UserExtended instance id that you what to check what formulary ids it have access

        Returns:
            django.db.models.QuerySet(int): Returns a queryset of form_ids
        """
        return self.get_queryset().filter(user_id=user_id).values_list('form_id', flat=True)