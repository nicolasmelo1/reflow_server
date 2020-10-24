from django.db import transaction

from reflow_server.theme.models import Theme, ThemeType, ThemeForm, \
    ThemeField, ThemeFieldOptions, ThemeKanbanDimensionOrder, ThemeKanbanCard, \
    ThemeKanbanCardField, ThemeNotificationConfiguration, ThemeNotificationConfigurationVariable, \
    ThemeDashboardChartConfiguration
from reflow_server.theme.services.data import ThemeReference

from reflow_server.formulary.models import Form, Field, FieldOptions
from reflow_server.kanban.models import KanbanDimensionOrder, KanbanCard, KanbanCardField
from reflow_server.notification.models import NotificationConfiguration, NotificationConfigurationVariable
from reflow_server.dashboard.models import DashboardChartConfiguration

import re


class ThemeUpdateService:
    def __init__(self):
        """
        Responsible for creating themes. Themes are created of a data that already exists.

        It is like a big ctrl+c/ctrl+v of the content of one table to another. When creating themes
        what we do is create themes based on the formularies the user have selected to copy the content from.

        On stuff like Kanban we get the kanban data of the current user that is editing. On stuff like NotificationConfiguration
        we just get the Notifications that is for the hole company.

        Available Methods:
            - .create_or_update(): creates or updates a theme instance
        """
        self.theme_reference = ThemeReference()
    
    def __create_or_update_theme(self, theme_type_id, display_name, is_public, description, user_id, company_id, theme_id=None):
        if not ThemeType.theme_.exists_theme_type_by_theme_type_id(theme_type_id):
            theme_type_id = ThemeType.theme_.empty_theme_type_id()

        return Theme.theme_.update_or_create(
            theme_id=theme_id,
            display_name=display_name,
            theme_type_id=theme_type_id,
            user_id=user_id,
            company_id=company_id,
            is_public=is_public,
            description=description
        )

    def __create_theme_forms(self, theme_instance, form_ids, company_id):
        """
        This creates the main ThemeForms of Form instances. What we do is filter all of the formularies that we want to copy 
        the content from the `form_ids`

        This creates the MAIN THEMEFORMS so the ones with depends_on = None

        Args:
            theme_instance (reflow_server.theme.models.Theme): The Theme instance you have created to be used here
            form_ids (list(int)): list of ints where each int is a Form instance id. (usually those are main forms, not section instance ids)
            company_id (int): The id of the company that is creating this theme

        Returns:
            bool: return True to indicate the formulary has been created
        """
        for formulary in Form.theme_.main_forms_by_company_id_and_form_ids(company_id, form_ids):
            theme_formulary_instance = ThemeForm.theme_.create_main_theme_form(
                theme_instance, 
                formulary.id,
                formulary.form_name,
                formulary.label_name,
                formulary.order,
                formulary.type
            )
            self.theme_reference.add_formulary_reference(formulary.id, theme_formulary_instance)
        return True

    def __create_theme_sections(self, theme_instance, form_ids, company_id):
        """
        This creates theme sections based of the Form instances that have depends_on in one of the `form_ids` parameter 

        There are two things important to understand:
        - `formulary_reference` dict is also updated with the sections, SO the `formulary_reference`
        holds the reference on Form instances, we DO NOT separate between sections and forms.
        - When the section has a conditional, we can't set the conditiona_on_field yet because we 
        haven't created the field just yet. Because of this we create a reference so after we added the 
        fields we can just add the proper conditionals. Each key of the dict is the field_id the conditional 
        references to and the value is the section instance to update.

        Args:
            theme_instance (reflow_server.theme.models.Theme): The Theme instance you have created to be used here
            form_ids (list(int)): list of ints where each int is a Form instance id. (usually those are main forms, not section instance ids)
            company_id (int): The id of the company that is creating this theme

        Returns:
            bool: return True to indicate the formulary has been created
        """
        for section in Form.theme_.section_forms_by_company_id_and_main_form_ids(company_id, form_ids):
            theme_formulary_section_instance = ThemeForm.theme_.create_section_theme_form(
                theme_instance, 
                section.form_name,
                section.label_name,
                section.order,
                section.type,
                self.theme_reference.get_formulary_reference(section.depends_on.id).id,
                section.conditional_type,
                section.conditional_value
            )
            self.theme_reference.add_formulary_reference(section.id, theme_formulary_section_instance)
            if section.conditional_on_field:
                self.theme_reference.add_section_conditionals_reference(section.conditional_on_field.id, theme_formulary_section_instance)
        return True

    def __create_theme_fields(self, form_ids, company_id):
        """
        This is really similar to ThemeSelect `.__create_fields()` method.
        The only difference is that we don't actually use a service here since this is the service to be used.

        This method is responsible for creating fields of all of the formularies and sections of a theme.
        
        - First when we create a `form` field type, so a field_type that references to a field of another form,
        we DO NOT create the reference right away. We need to wait the creation of all of the fields. THEN we can
        add the specific references.
        - Second, conditionals are bound to a specific field. Like the first item, we also wait the creation of EVERY
        field to add the conditional fields. That's why we use the `section_conditionals_reference` parameter to.

        Last but not least, after all of the fields have been created we append the created fields to the field_reference
        on the ThemeReference object. return a dict to be used as reference. 

        Args:
            form_ids (list(int)): list of ints where each int is a Form instance id.
            company_id (int): The id of the company that is creating this theme

        Returns:
            bool: return True to indicate everything has been created
        """
        form_field_as_option_reference = {}
        formula_reference = {}
        formula_fields = []
        form_field_type_fields = []

        for field in Field.theme_.fields_by_company_id_and_main_form_ids(company_id, form_ids):
            #field_ids_in_formula = re.findall(r'{{(\w+)?}}', field.formula_configuration)
            #for field_id_in_formula in field_ids_in_formula:
            #    formula_configuration = formula_configuration.replace('{{'+field_id_in_formula+'}}', '{{'++'}}')
            theme_field_intance = ThemeField.theme_.create_theme_field(
                name=field.name,
                label_name=field.label_name,
                order=field.order,
                form=self.theme_reference.get_formulary_reference(field.form_id),
                field_type=field.type,
                placeholder=field.placeholder,
                field_is_hidden=field.field_is_hidden,
                label_is_hidden=field.label_is_hidden,
                required=field.required,
                is_unique=field.is_unique,
                date_configuration_auto_create=field.date_configuration_auto_create,
                date_configuration_auto_update=field.date_configuration_auto_update,
                number_configuration_allow_negative=field.number_configuration_allow_negative,
                number_configuration_allow_zero=field.number_configuration_allow_zero,
                date_configuration_date_format_type=field.date_configuration_date_format_type,
                period_configuration_period_interval_type=field.period_configuration_period_interval_type,
                number_configuration_number_format_type=field.number_configuration_number_format_type,
                formula_configuration=field.formula_configuration
            )
            
            self.theme_reference.add_field_reference(field.id, theme_field_intance)
            
            # If the field is of type `form` what we do is create a reference to it, so the key of the dict
            # is the field.id and the value is the field instance we should update.
            # On the other hand, we also append the field to a list, so we know the `form_field_as_option_id`
            # of this field. 
            # If you notice, ALL of the fields created, are created without the reference on the `form` field type. 
            # Because of this, we get the field that is of this type, and resolves the reference after every field 
            # has already been created
            if field.form_field_as_option not in (None, '') and field.type.type == 'form':
                form_field_as_option_reference[field.id] = theme_field_intance
                form_field_type_fields.append(field)
            
            # When a formula exists in a field we need to update its references since it is a string.
            if field.formula_configuration not in (None, ''):
                formula_reference[field.id] = theme_field_intance
                formula_fields.append(field)
            
            # if the field is of type `option` or `multi_option` we add the options to the ThemeFieldOptions
            # object model.
            if field.type.type in ['option', 'multi_option']:
                for field_option in FieldOptions.theme_.field_options_by_field_id(field.id):
                    ThemeFieldOptions.theme_.create_theme_field_option(
                        theme_field_intance, field_option.option, field_option.order
                    )

        for field_id, theme_section in self.theme_reference.get_section_conditionals_reference():
            ThemeForm.theme_.update_section_conditional_on_field(theme_section.id, self.theme_reference.get_field_reference(field_id).id)

        for field in form_field_type_fields:
            theme_field = form_field_as_option_reference[field.id]
            ThemeField.theme_.update_theme_field_form_field_as_option(theme_field.id, self.theme_reference.get_field_reference(field.form_field_as_option_id).id)

        for field in formula_fields:
            theme_field = formula_reference[field.id]

            formula_configuration = field.formula_configuration
            field_ids_in_formula = re.findall(r'{{(\w+)?}}', formula_configuration)
            for field_id_in_formula in field_ids_in_formula:
                formula_configuration = formula_configuration.replace(
                    '{{'+field_id_in_formula+'}}', 
                    '{{'+str(self.theme_reference.get_field_reference(int(field_id_in_formula)).id)+'}}'
                )
            
            ThemeField.theme_.update_theme_field_formula_configuration(theme_field.id, formula_configuration)

        return True

    def __create_theme_kanban(self, theme_instance, form_ids, company_id, user_id):
        """
        Responsible for creating the kanban configuration for this template, this uses the user default configuration.
        This function creates the ThemeKanbanDimensionOrder with the dimension and the order of the columns, and also 
        the ThemeKanbanCard with its respective fields ordered.

        Args:
            theme_instance (reflow_server.theme.models.Theme): The Theme instance you have created to be used here
            form_ids (list(int)): list of ints where each int is a Form instance id.
            company_id (int): The id of the company that is creating this theme
            user_id (int): The id of the user that is creating this theme

        Returns:
            bool: return True to indicate everything has been created
        """
        kanban_card_ids = KanbanCardField.theme_.kanban_card_ids_by_user_id_company_id_and_main_form_ids(user_id, company_id, form_ids)
        kanban_dimension_orders = KanbanDimensionOrder.theme_.kanban_dimension_order_by_user_id_company_id_and_main_form_ids(user_id, company_id, form_ids)
        kanban_cards = KanbanCard.theme_.kanban_cards_by_kanban_card_ids(kanban_card_ids)

        for kanban_dimension_order in kanban_dimension_orders:
            ThemeKanbanDimensionOrder.theme_.create_theme_kanban_dimension_order(
                theme_instance, self.theme_reference.get_field_reference(kanban_dimension_order.dimension.id).id, 
                kanban_dimension_order.options, kanban_dimension_order.order, kanban_dimension_order.default
            )

        for kanban_card in kanban_cards:
            theme_kanban_card = ThemeKanbanCard.theme_.create_theme_kanban_card(
                theme_instance, kanban_card.default
            )

            for kanban_card_field in KanbanCardField.theme_.kanban_card_fields_by_kanban_card_id_ordered_by_id(kanban_card.id):
                ThemeKanbanCardField.theme_.create_theme_kanban_card_field(theme_kanban_card.id, self.theme_reference.get_field_reference(kanban_card_field.field.id).id)
        return True

    def __create_theme_notification(self, theme_instance, form_ids, company_id, user_id):
        """
        Creates the ThemeNotificationsConfiguration instances based on NotificationConfigurations of the user
        for this specific company and that are for the hole company.

        Args:
            theme_instance (reflow_server.theme.models.Theme): The Theme instance you have created to be used here
            form_ids (list(int)): list of ints where each int is a Form instance id.
            company_id (int): The id of the company that is creating this theme
            user_id (int): The id of the user that is creating this theme

        Returns:
            bool: return True to indicate everything has been created
        """
        for notification_configuration in NotificationConfiguration.theme_.notification_configurations_for_company_by_user_id_company_id_and_main_form_ids(user_id, company_id, form_ids):
            theme_notification_configuration = ThemeNotificationConfiguration.theme_.create_theme_notification_configuration(
                field_id=self.theme_reference.get_field_reference(notification_configuration.field.id).id,
                form_id=self.theme_reference.get_formulary_reference(notification_configuration.form.id).id,
                for_company=notification_configuration.for_company,
                name=notification_configuration.name,
                text=notification_configuration.text,
                days_diff=notification_configuration.days_diff
            )

            for notification_configuration_variable in NotificationConfigurationVariable.theme_.notification_configuration_variables_by_notification_configuration_id_ordered_by_order(notification_configuration.id):
                ThemeNotificationConfigurationVariable.theme_.create_theme_notification_configuration_variable(
                    notification_configuration_variable.order,
                    theme_notification_configuration.id,
                    self.theme_reference.get_field_reference(notification_configuration_variable.field.id).id
                )
        return True
    
    def __create_theme_dashboard(self, theme_instance, form_ids, company_id, user_id):
        """
        Creates the ThemeDashboardChartConfiguration instances based on DashboardChartConfiguration of the user
        for this specific company and that are for the hole company. (so the ones with for_company = True)

        Args:
            theme_instance (reflow_server.theme.models.Theme): The Theme instance you have created to be used here
            form_ids (list(int)): list of ints where each int is a Form instance id.
            company_id (int): The id of the company that is creating this theme
            user_id (int): The id of the user that is creating this theme

        Returns:
            bool: return True to indicate everything has been created
        """
        for dashboard_chart_configuration in DashboardChartConfiguration.theme_.dashboard_chart_configurations_by_company_id_main_form_ids_user_id_for_hole_company_ordered(company_id, form_ids, user_id):
            theme_dashboard_chart_configuration = ThemeDashboardChartConfiguration.theme_.create_theme_dashboard_chart_configuration(
                dashboard_chart_configuration.name,
                dashboard_chart_configuration.for_company,
                self.theme_reference.get_field_reference(dashboard_chart_configuration.value_field.id).id,
                self.theme_reference.get_field_reference(dashboard_chart_configuration.label_field.id).id,
                dashboard_chart_configuration.number_format_type.id,
                dashboard_chart_configuration.chart_type.id,
                dashboard_chart_configuration.aggregation_type.id,
                self.theme_reference.get_formulary_reference(dashboard_chart_configuration.form.id).id,
                theme_instance.id
            )
        return True

    @transaction.atomic
    def create_or_update(self, theme_type_id, display_name, is_public, description, user_id, company_id, form_ids=[], theme_id=None):
        """
        This method is used for creating or updating theme templates. It's nice to notice and understand that
        IF YOU ARE UPDATING AN INTANCE AND SETTING FORM_IDS WE RECREATE THE THEME.

        What this means is that, if the form_ids list is not empty and theme_id is not None we remove the Theme instance
        and then creates it again.

        If the Theme has been created, then we create the formularies, fields, kanban, notifications and so on bound to the theme.

        With this we can always edit the theme but keep all of the formularies content intact.

        Args:
            theme_type_id (int): this an existing reflow_server.theme.models.ThemeType instance id
            display_name (str): The name of your template, what you want to show
            is_public (bool): Public means users will be able to see the templates.
            description (str): A simple description of what the template do
            user_id (int): What user is creating this template, for some data we will use the data of this specific user.
            company_id (int): The company where the user is editing the templates
            form_ids (list(int), optional): This is only optional when editing themes, otherwise it is obligatory. It holds the main formulary ids to create
                                       templates from. Defaults to [].
            theme_id (int, optional): This is a Theme intance id, used only when editing an existing instance. Defaults to None.

        Raises:
            AttributeError: `form_ids` parameter is only optional when editing an Theme instance, otherwise it is obligatory.

        Returns:
            bool: return True to indicate everything went fine
        """
        if not theme_id and not form_ids:
            raise AttributeError('Looks like you are not updating a template and have not set the `form_ids` parameter, '
                                 'the `form_ids` attribute cannot be empty when creating templates.')

        # if we are updating a theme and it has form_ids to set we delete the theme and create everything again, this way
        # we keep all of the theme data "written in stone"
        if theme_id and len(form_ids) > 0:
            Theme.theme_.delete_theme_by_theme_id(theme_id)
        theme_instance, has_created_theme = self.__create_or_update_theme(theme_type_id, display_name, is_public, description, user_id, company_id, theme_id)
        # we only create the formulary and the fields and so on if the theme has just been created. otherwise we NEVER update the formularies.
        # this way we can actually edit the theme description, name and set if is public or not but without touching the coontent of the theme.
        if has_created_theme:
            self.__create_theme_forms(theme_instance, form_ids, company_id)
            self.__create_theme_sections(theme_instance, form_ids, company_id)
            self.__create_theme_fields(form_ids, company_id)

            self.__create_theme_kanban(theme_instance, form_ids, company_id, user_id)
            self.__create_theme_notification(theme_instance, form_ids, company_id, user_id)
            self.__create_theme_dashboard(theme_instance, form_ids, company_id, user_id)
        return theme_instance