from django.db import models


class ThemeNotificationConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_notification_configurations_by_theme_id(self, theme_id):
        """
        Retrieves a queryset of ThemeNotificationConfiguration instances from a particular theme

        Args:
            theme_id (int): From which Theme instance id the ThemeNotificationConfiguration are from.

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.ThemeNotificationConfiguration): A queryset
            of ThemeNotificationConfiguration instances from a particular theme
        """
        return self.get_queryset().filter(field__form__depends_on__theme_id=theme_id)
    
    def create_theme_notification_configuration(self, field_id, form_id, for_company, name, text, days_diff):
        """
        This creates a ThemeNotificationConfiguration instance

        Args:
            for_company (bool): Sets the notification configuration for the hole company 
            name (str): Just a placeholder and user friendly name for the notification configuration, setted by the user
            text (str): The text of the notification configuration, it's important to understand it also could contain variables
                        if that's the case, use `.add_notification_variable()` method to add variables.
            days_diff (int): The number of the difference of days to notify. So you could notify the user on the same day, sixty
                             days earlier of the date, or even sixty days after the date
            form_id (int): What ThemeForm does this theme_notification_configuration references to
            field_id (int): From what `date` theme_field_type theme_field does this notification configuration references to

        Returns:
            reflow_server.theme.models.ThemeNotificationConfiguration: The created ThemeNotificationConfiguration instance
        """
        return self.get_queryset().create(
            field_id=field_id,
            form_id=form_id,
            for_company=for_company,
            name=name,
            text=text,
            days_diff=days_diff
        )