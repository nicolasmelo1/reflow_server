from django.db import models


class ThemeFormThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_form_by_theme_id_and_theme_form_id(self, theme_id, theme_form_id):
        """
        Gets a ThemeForm instance from a theme_id and a theme_form_id. It's important to notice
        that this doesn't care whether it is a main form or a section.

        Args:
            theme_id (int): The theme this ThemeForm instance is from
            theme_form_id (int): The theme form id to retrieve

        Returns:
            reflow_server.theme.models.ThemeForm: The theme form instance.
        """
        return self.get_queryset().filter(id=theme_form_id, theme_id=theme_id).first()

    def main_theme_forms_by_theme_id(self, theme_id):
        """
        Gets a queryset of main_forms, this means ThemeForm instances where depends_on is null.

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeForm is from.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeForm): A queryset of ThemeForm instances
        """
        return self.get_queryset().filter(theme_id=theme_id, depends_on__isnull=True)

    def sections_theme_forms_by_theme_id(self, theme_id):
        """
        Get queryset of sections of ThemeForm. Remember that sections are the ThemeForm with depends_on
        that equals NULL

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeForm is from.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeForm): A queryset of ThemeForm instances
        """
        return self.get_queryset().filter(theme_id=theme_id, depends_on__isnull=False)

    def create_main_theme_form(self, theme_instance, form_id, form_name, label_name, order, form_type):
        """
        Creates a main form theme instance. Those ThemeForms created here are the ones that have
        depends_on=None

        Args:
            theme_instance (reflow_server.theme.models.Theme): The created theme instance this theme form is bound to.
            form_id (int): The id of the formulary it is based on so we can then know on what form this was based on.
            form_name (str): The name of the formulary, it is actually not needed since we create a new name when create a new Form of
                             ThemeForm. This is like an id so it needs to be unique for the hole company, that's because of this that 
                             we do not use this as is.
            label_name (str): The name of the formulary that is displayed to the user.
            order (int): The order of the formulary, which comes first, which comes second and so on.
            form_type (reflow_server.formulary.models.FormType): The form_type instance, it is always the same so anyway.

        Returns:
            reflow_server.theme.models.ThemeForm: The newly created ThemeForm instance
        """
        return self.get_queryset().create(
            theme=theme_instance, 
            form_id=form_id,
            form_name=form_name,
            label_name=label_name,
            order=order,
            type=form_type
        )

    def create_section_theme_form(self, theme_instance, form_name, label_name, order, form_type, depends_on_id, conditional_type=None, conditional_value=None):
        """
        Creates a section ThemeForm instance. Sections are ThemeForm instances that have depends_on=None.
        We do not update the conditional_on_field here, instead you update it after the fields have been created.

        Args:
            theme_instance (reflow_server.theme.models.Theme): The created theme instance this theme form is bound to.
            form_id (int): The id of the formulary it is based on so we can then know on what form this was based on.
            form_name (str): The name of the formulary, it is actually not needed since we create a new name when create a new Form of
                             ThemeForm. This is like an id so it needs to be unique for the hole company, that's because of this that 
                             we do not use this as is.
            label_name (str): The name of the formulary that is displayed to the user.
            order (int): The order of the formulary, which comes first, which comes second and so on.
            form_type (reflow_server.formulary.models.FormType): The FormType instance, it can be multi-form or form instances right now
                                                                 you can check form_type instance for further reference.
            depends_on_id (int): Another ThemeForm instance id. This is the formulary instance that the section is bound to.
            conditional_type (reflow_server.formulary.models.ConditionalType, optional): A conditional type representing what is the conditional, 
                                                                                         can be 'equal', 'different' and so on. You can check the 
                                                                                         model and the database to see the options available.
                                                                                         Defaults to None.
            conditional_value (str, optional): On what conditional value this conditional activates. Defaults to None.
        """
        return self.get_queryset().create(
            theme=theme_instance, 
            form_name=form_name,
            depends_on_id=depends_on_id,
            label_name=label_name,
            order=order,
            type=form_type,
            conditional_type=conditional_type,
            conditional_value=conditional_value
        )

    def update_section_conditional_on_field(self, theme_form_section_id, field_id):
        """
        Updates the condiditional_on_field attribute of a single ThemeForm section instance based on its id 

        Args:
            theme_form_section_id (int): The id of the ThemeForm you want to update. Usually, this id is of an instance
                                         that has ThemeForm depends_on=None
            field_id (int): The id of the field you want to use as conditional for this section

        Returns:
            int: Returns the number of affected rows, usually 1: https://docs.djangoproject.com/en/dev/ref/models/querysets/#update
        """
        return self.get_queryset().filter(id=theme_form_section_id, depends_on__isnull=False).update(conditional_on_field_id=field_id)