from django.db import models


class NotificationConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def notification_configurations_for_company_by_user_id_company_id_and_main_form_ids(self, user_id, company_id, main_form_ids):
        """
        Retrieves the NotificationConfiguration instances of a company, a user and from a list of formulary ids that are for the hole company

        Args:
            user_id (int): A UserExtended instance id, this is used to filter NotificationConfigurations for a specific user.
            company_id (int): A Company instance id, from which company is this notification configuration
            main_form_ids (list(int)): The formularies ids to filter the notification configuration

        Returns:
            django.db.models.QuerySet(reflow_server.notification.models.NotificationConfiguration): Returns a queryset of NotificationConfiguration
                                                                                             instances from the parameters provided.
        """
        return self.get_queryset().filter(
            field__form__depends_on__group__company_id=company_id, 
            user_id=user_id, 
            field__form__depends_on__in=main_form_ids, for_company=True
        )