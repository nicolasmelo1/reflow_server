from django.db import models


class ThemeThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def themes_by_company_type_name(self, company_type_name):
        """
        Gets themes based on the theme type groups. `design`, `marketing` and so on.

        Args:
            company_type_name (str): The name of the group. Check `company_type` table
            for reference

        Returns:
            django.db.QuerySet(reflow_server.theme.models.Theme): The queryset of the themes of the group
        """
        return self.get_queryset().filter(company_type__name=company_type_name)

    def theme_by_theme_id(self, theme_id):
        """
        Retrives a single Theme instance by the theme id

        Args:
            theme_id (int): The Theme instance id to retrieve

        Returns:
            reflow_server.theme.models.Theme: The Theme instance retrieved by its id.
        """
        return self.get_queryset().filter(id=theme_id).first()

    def update_or_create(self, display_name, theme_type_id, user_id, is_public, description, theme_id=None):
        """
        Updates or creates a single theme instance. If theme_id is defined we update, otherwise we 
        create a new instance.

        Args:
            theme_type_id (int): this an existing reflow_server.theme.models.ThemeType instance id
            display_name (str): The name of your template, what you want to show
            is_public (bool): Public means users will be able to see the templates.
            description (str): A simple description of what the template do
            user_id (int): What user is creating this template, for some data we will use the data of this specific user.
            theme_id (int, optional): This is a Theme intance id, used only when editing an existing instance. Defaults to None.

        Returns:
            tuple(reflow_server.theme.models.Theme, bool): The Theme instance created
        """
        return self.get_queryset().update_or_create(id=theme_id, defaults={
            'display_name': display_name,
            'company_type_id': theme_type_id,
            'user_id': user_id,
            'is_public': is_public,
            'description': description
        })

    def delete_theme_by_theme_id(self, theme_id):
        """
        Deletes a single Theme instance by it's id.

        Args:
            theme_id (int): The Theme instance id to remove
        """
        return self.theme_by_theme_id(theme_id).delete()