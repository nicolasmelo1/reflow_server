from django.db import models


class ThemeFieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_fields_by_theme_id(self, theme_id):
        """
        Returns a queryset of ThemeField instances based on a theme_id

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeField is from.

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.ThemeField): A queryset of ThemeField instances
            from the theme_id
        """
        return self.get_queryset().filter(form__depends_on__theme_id=theme_id)

    def create_theme_field(self, name, label_name, order, form, field_type, 
                           placeholder=None, field_is_hidden=False, label_is_hidden=False, required=False, 
                           is_unique=False, date_configuration_auto_create=False, date_configuration_auto_update=False, 
                           number_configuration_allow_negative=True, number_configuration_allow_zero=True, 
                           date_configuration_date_format_type=None, period_configuration_period_interval_type=None, 
                           number_configuration_number_format_type=None, formula_configuration=None):
        """
        Creates a new ThemeField instance based on a Field instance.

        Args:
            name (str): The name of the field, this is similar to ThemeForm name, this is not used when the user selects
                        since it works like an id for every company we create when creating a new field for the user.
            label_name (str): This is the name the user sees on the field. It usually what he have access to
            order (int): The ordering of the field, which comes first, which is second and so on.
            form (reflow_server.theme.models.ThemeForm): The ThemeForm section instance this field is bounded to.
            field_type (reflow_server.formulary.models.FieldType): The type of this field, can be `number`, `text`, `form` and so on. 
                                                                   You should check the `field_type` table in the database for reference.
            placeholder (str, optional): The placeholder of the field, it is the text that is shown before the value is written. Defaults to None.
            field_is_hidden (bool, optional): The field is shown or not?. Defaults to False.
            label_is_hidden (bool, optional): The label of the field, so 'label_name' is shown or not?. Defaults to False.
            required (bool, optional): Is this field required. Defaults to False.
            is_unique (bool, optional): Is the value of the field unique (Can't be equal values of this field). Defaults to False.
            date_configuration_auto_create (bool, optional): Automatically adds a date when the user creates the formulary data. Defaults to False.
            date_configuration_auto_update (bool, optional): Automatically adds a date when the user updates the formulary data. Defaults to False.
            number_configuration_allow_negative (bool, optional): Number can be negative or just positive. Defaults to True.
            number_configuration_allow_zero (bool, optional): 0 is a valid number or not. Defaults to True.
            date_configuration_date_format_type (reflow_server.formulary.models.FieldDateFormatType, optional): The format of the date, does it contains hours or not.
                                                                                                                Defaults to None.
            period_configuration_period_interval_type (reflow_server.formulary.models.FieldPeriodIntervalType, optional): The period format, only for 'period' field types. 
                                                                                                                          Defaults to None.
            number_configuration_number_format_type (reflow_server.formulary.models.FieldNumberFormatType, optional): The number formating, can be percentage, currency and so on. 
                                                                                                                      Defaults to None.
            formula_configuration (str, optional): The formula configuration, you should check `formula` app for reference on what are formulas. Defaults to None.

        Returns:
            reflow_server.theme.models.ThemeField: The newly created field instance.
        """
        return self.get_queryset().create(
            name=name,
            label_name=label_name,
            order=order,
            form=form,
            type=field_type,
            placeholder=placeholder,
            field_is_hidden=field_is_hidden,
            label_is_hidden=label_is_hidden,
            required=required,
            is_unique=is_unique,
            date_configuration_auto_create=date_configuration_auto_create,
            date_configuration_auto_update=date_configuration_auto_update,
            number_configuration_allow_negative=number_configuration_allow_negative,
            number_configuration_allow_zero=number_configuration_allow_zero,
            date_configuration_date_format_type=date_configuration_date_format_type,
            period_configuration_period_interval_type=period_configuration_period_interval_type,
            number_configuration_number_format_type=number_configuration_number_format_type,
            formula_configuration=formula_configuration,
            number_configuration_mask=None,
            form_field_as_option=None
        )
    
    def update_theme_field_form_field_as_option(self, theme_field_id, form_field_as_option_id):
        """
        This is used for just updating the form_field_as_option parameter of a single ThemeField instance.
        We know the ThemeField instance to update because of the `theme_field_id` parameter

        Args:
            theme_field_id (int): This is the id of the ThemeField instance you want to update
            form_field_as_option_id (int): An id of a ThemeField instance, this id is the field from what formulary
                                           you want to use as option.

        Returns:
            int: Returns the number of affected rows, usually 1: https://docs.djangoproject.com/en/dev/ref/models/querysets/#update
        """
        return self.get_queryset().filter(id=theme_field_id).update(form_field_as_option_id=form_field_as_option_id)
        