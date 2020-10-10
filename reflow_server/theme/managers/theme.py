from django.db import models


class ThemeThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def themes_by_user_and_company_ordered_by_id(self, company_id, user_id):
        """
        Gets themes from a specific user at a specific company ordered by the last id to the first id.

        Args:
            company_id (int): From what company the template you are loading is from
            user_id (int): What user has created this template

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.Theme): A queryset of themes
                                                                  from a user at a specific
                                                                  company
        """
        return self.get_queryset().filter(user_id=user_id, company_id=company_id).order_by('-id')

    def themes_by_theme_type_name(self, theme_type_name):
        """
        Gets themes based on the theme type groups. `design`, `marketing` and so on.

        Args:
            theme_type_name (str): The name of the group. Check `theme_type` table
            for reference

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.Theme): The queryset of the themes of the group
        """
        return self.get_queryset().filter(theme_type__name=theme_type_name)

    def exists_theme_by_theme_id_user_id_and_company_id(self, theme_id, user_id, company_id):
        """
        Check if a theme id of particular user at a particular company exists.

        Args:
            theme_id (int): The Theme instance id to check
            company_id (int): From what company the template you are loading is from
            user_id (int): What user has created this template

        Returns:
            bool: Returns true if exists and false if not
        """
        return self.themes_by_user_and_company_ordered_by_id(company_id, user_id).filter(id=theme_id).exists()

    def theme_by_theme_id(self, theme_id):
        """
        Retrives a single Theme instance by the theme id

        Args:
            theme_id (int): The Theme instance id to retrieve

        Returns:
            reflow_server.theme.models.Theme: The Theme instance retrieved by its id.
        """
        return self.get_queryset().filter(id=theme_id).first()

    def update_or_create(self, display_name, theme_type_id, user_id, company_id, is_public, description, theme_id=None):
        """
        Updates or creates a single theme instance. If theme_id is defined we update, otherwise we 
        create a new instance.

        Args:
            theme_type_id (int): this an existing reflow_server.theme.models.ThemeType instance id
            display_name (str): The name of your template, what you want to show
            is_public (bool): Public means users will be able to see the templates.
            description (str): A simple description of what the template do
            company (int): From what company is this theme from.
            user_id (int): What user is creating this template, for some data we will use the data of this specific user.
            theme_id (int, optional): This is a Theme intance id, used only when editing an existing instance. Defaults to None.

        Returns:
            tuple(reflow_server.theme.models.Theme, bool): The Theme instance created
        """
        return self.get_queryset().update_or_create(id=theme_id, defaults={
            'display_name': display_name,
            'theme_type_id': theme_type_id,
            'user_id': user_id,
            'company_id': company_id,
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