from django.db import transaction

from reflow_server.theme.models import Theme, ThemeForm, ThemeField, ThemeFieldOptions, ThemeKanbanDefault, \
    ThemeKanbanCard, ThemeKanbanCardField, ThemeNotificationConfiguration, ThemeNotificationConfigurationVariable, \
    ThemeDashboardChartConfiguration, ThemeFormulaVariable
from reflow_server.theme.services.data import ThemeReference
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.models import Field, Form

from reflow_server.formulary.services.data import FieldOptionsData, FormulaVariableData
from reflow_server.formulary.services.group import GroupService
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService
from reflow_server.kanban.services import KanbanCardService, KanbanService
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService
from reflow_server.dashboard.services.dashboard_configuration import DashboardChartConfigurationService

import re


class ThemeSelectService:
    def __init__(self, theme_id, company_id, user_id):
        """
        This is responsible for selecting themes.

        Args:
            theme_id (int): A Theme instance is, what theme the user have selected
            company_id (int): A Company instance id, for what company the user has selected the template
            user_id (int): A UserExtended instance id, this is the user that has selected the template
        """
        self.theme = Theme.theme_.theme_by_theme_id(theme_id)
        self.company_users = UserExtended.theme_.users_active_by_company_id(company_id)
        self.company_id = company_id
        self.user_id = user_id
        self.theme_reference = ThemeReference()
        
    def __create_group(self):
        """
        Creates the group. It's important to notice that groups have the theme_type name on it 
        and not the theme name. So if this theme is on the section `Sales` and the name of the theme is
        `Sales for Startups`. The name will be `Sales` and NOT `Sales for startups`

        Returns:
            reflow_server.formulary.models.Group: The newly created group instance that will holds all of the formularies
            created of this template/theme.
        """
        group_service = GroupService(self.company_id)
        return group_service.create_group(self.theme.theme_type.label_name)

    def __create_forms(self, group):
        """
        This is used for creating formularies. Formularies are based on the ThemeForm and here THEY ARE NOT SECTIONS.
        This means that depends_on is NULL.

        This creates a dict that will serve as reference for ThemeForm, so everywhere that has a reference for ThemeForm
        we can use this reference dict.

        Args:
            group (reflow_server.models.formulary.Group): The Group instance created that will hold all of the 
            formularies created here.

        Returns:
            bool: returns True indicating the formularies and references where created.
        """
        formulary_service = FormularyService(self.user_id, self.company_id)

        for theme_form in ThemeForm.theme_.main_theme_forms_by_theme_id(self.theme.id):
            formulary_instance = formulary_service.save_formulary(True, theme_form.label_name, theme_form.order, group)
            self.theme_reference.add_formulary_reference(theme_form.id, formulary_instance)
        
        return True

    def __create_sections(self):
        """
        This creates sections of the ThemeForm instances that have depends_on as not null.
        We use the SectionService for creating sections so it can handle most of the business logic.

        There are two things important to understand:
        - `formulary_reference` dict is also updated with the sections, SO the `formulary_reference`
        holds the reference on ThemeForm instances, we DO NOT separate between sections and forms.
        - When the section has a conditional, we can't set the conditiona_on_field yet because we 
        haven't created the field just yet. Because of this we create a reference so after we added the 
        fields we can just add the proper conditionals. Each key of the dict is the field_id the conditional 
        references to and the value is the section instance to update.

        Returns:
            bool: returns True to indicate that everything went fine.
        """
        for theme_section in ThemeForm.theme_.sections_theme_forms_by_theme_id(self.theme.id):
            section_service = SectionService(
                user_id=self.user_id, 
                company_id=self.company_id, 
                form_id=self.theme_reference.get_formulary_reference(theme_section.depends_on.id).id
            )
                
            section = section_service.save_section(
                enabled=True, 
                label_name=theme_section.label_name, 
                order=theme_section.order, 
                show_label_name=theme_section.show_label_name,
                conditional_excludes_data_if_not_set=theme_section.conditional_excludes_data_if_not_set,
                conditional_value=theme_section.conditional_value,
                section_type=theme_section.type,
                conditional_type=theme_section.conditional_type, 
                conditional_on_field=None
            )
            self.theme_reference.add_formulary_reference(theme_section.id, section)
            if theme_section.conditional_on_field:
                self.theme_reference.add_section_conditionals_reference(theme_section.conditional_on_field.id, section)
        return True
    
    def __create_fields(self):
        """
        This method is responsible for creating fields of all of the formularies and sections of a theme.
        
        - First when we create a `form` field type, so a field_type that references to a field of another form,
        we DO NOT create the reference right away. We need to wait the creation of all of the field. THEN we can
        add the specific references.
        - Second, conditionals are bound to a specific field. Like the first item, we also wait the creation of EVERY
        field to add the conditional fields. That's why we use the `section_conditionals_reference` parameter to.

        Last but not least, after all of the fields have been created we append the created fields to the field_reference
        on the ThemeReference object. return a dict to be used as reference. 

        Returns:
            bool: returns True indicating all fields were created
        """
        form_field_as_option_reference = {}
        form_field_type_fields = []
        formula_fields = []

        for theme_field in ThemeField.theme_.theme_fields_by_theme_id(self.theme.id):
            field_options_data = FieldOptionsData()

            # if the field is of type `option` or `multi_option` we get the options of the theme to add on the field.
            # initially the `field_options_data` holds just an empty list, but if it is from both types we use the
            # options saved.
            if theme_field.type.type in ['option', 'multi_option']:
                for option in ThemeFieldOptions.theme_.options_by_theme_field_id(theme_field_id=theme_field.id):
                    field_options_data.add_field_option(option)
            
            field_service = FieldService(
                user_id=self.user_id, 
                company_id=self.company_id, 
                form_id=self.theme_reference.get_formulary_reference(theme_field.form.depends_on.id).id
            )

            field = field_service.save_field(
                enabled=True, 
                label_name=theme_field.label_name, 
                order=theme_field.order, 
                is_unique=theme_field.is_unique, 
                field_is_hidden=theme_field.field_is_hidden, 
                label_is_hidden=theme_field.label_is_hidden, 
                placeholder=theme_field.placeholder, 
                required=theme_field.required, 
                section=self.theme_reference.get_formulary_reference(theme_field.form_id),
                form_field_as_option=None, 
                is_long_text_a_rich_text=theme_field.is_long_text_rich_text,
                formula_configuration=theme_field.formula_configuration, 
                date_configuration_auto_create=theme_field.date_configuration_auto_create, 
                date_configuration_auto_update=theme_field.date_configuration_auto_update,
                number_configuration_number_format_type=theme_field.number_configuration_number_format_type, 
                date_configuration_date_format_type=theme_field.date_configuration_date_format_type, 
                period_configuration_period_interval_type=theme_field.period_configuration_period_interval_type, 
                field_type=theme_field.type, 
                field_options_data=field_options_data
            )

            self.theme_reference.add_field_reference(theme_field.id, field)

            # If the theme_field is of type `form` what we do is create a reference to it, so the key of the dict
            # is the theme_field.id and the value is the field instance we should update.
            # On the other hand, we also appends the theme_field to a list, so we know the `form_field_as_option_id`
            # of this theme_field. 
            # If you notice, ALL of the fields created, are created without the reference on the `form` field type. 
            # Because of this, we get the field that is of this type, and resolves the reference after every field 
            # has already been created
            if theme_field.form_field_as_option not in (None, '') and theme_field.type.type == 'form':
                form_field_as_option_reference[theme_field.id] = field
                form_field_type_fields.append(theme_field)

            # When a formula exists in a field we need to update its references since it is a string.
            if theme_field.formula_configuration not in (None, ''):
                formula_fields.append(theme_field)
                
        # set conditionals on sections
        for conditional_reference in self.theme_reference.get_section_conditionals_reference():
            Form.theme_.update_section_conditional_on_field(
                conditional_reference['instance'].id, 
                self.theme_reference.get_field_reference(conditional_reference['reference_id']).id
            )

        # set form_field_as_option on fields
        for theme_field in form_field_type_fields:
            field = form_field_as_option_reference[theme_field.id]
            Field.theme_.update_field_form_field_as_option_id(field.id, self.theme_reference.get_field_reference(theme_field.form_field_as_option_id).id)

        for theme_field in formula_fields:
            theme_formula_variable_ids = ThemeFormulaVariable.theme_.variable_ids_by_theme_field_id(theme_field.id)
            field_instance = self.theme_reference.get_field_reference(theme_field.id)
            
            field_service = FieldService(
                user_id=self.user_id, 
                company_id=self.company_id, 
                form_id=self.theme_reference.get_formulary_reference(theme_field.form.depends_on.id).id
            )

            formula_variable_ids = [
                FormulaVariableData(self.theme_reference.get_formulary_reference(theme_formula_variable_id).id)
                for theme_formula_variable_id in theme_formula_variable_ids
            ]

            field_service.save_formula_variables(field_instance, formula_variable_ids)
        return True

    def __create_kanban(self):
        """
        Create the kanban dimnesion order values for all of the users of the company and also creates
        the KanbanCard for all of the users.
        This method defines kanban defaults so when the user opens the kanban we can already know its 
        default kanban card and also the default kanban dimension.

        Returns:
            bool: Return True to indicate everything went fine.
        """
        theme_kanban_cards = ThemeKanbanCard.theme_.theme_kanban_cards_by_theme_id(self.theme.id)
        theme_kanban_defaults = ThemeKanbanDefault.theme_.theme_kanban_defaults_by_theme_id(self.theme.id)
        for user in self.company_users:
            kanban_card_service = KanbanCardService(user_id=user.id)
           
            for theme_kanban_card in theme_kanban_cards:
                theme_kanban_card_field_ids = ThemeKanbanCardField.theme_.theme_field_ids_by_theme_kanban_card_id(theme_kanban_card.id)
                kanban_card_field_ids = [self.theme_reference.get_field_reference(theme_kanban_card_field_id).id 
                                         for theme_kanban_card_field_id in theme_kanban_card_field_ids]

                # we create a new kanban card with it's fields, and then we set the default of the instance created
                # to be equal the theme_kanban_card default
                kanban_card_instance = kanban_card_service.save_kanban_card(kanban_card_field_ids)
                self.theme_reference.add_kanban_card_reference(theme_kanban_card.id, kanban_card_instance)
            
            # Adds all of the defaults for all of the users of the company
            for theme_kanban_default in theme_kanban_defaults:
                kanban_service = KanbanService(user.id, self.company_id, form=self.theme_reference.get_formulary_reference(theme_kanban_default.form.id))
                default_kanban_card_id = self.theme_reference.get_kanban_card_reference(theme_kanban_default.kanban_card.id).id
                default_kanban_dimension_id = self.theme_reference.get_field_reference(theme_kanban_default.kanban_dimension.id).id
                
                if kanban_service.are_defaults_valid(default_kanban_card_id, default_kanban_dimension_id):
                    kanban_service.save_defaults(default_kanban_card_id, default_kanban_dimension_id)
        return True

    def __create_notification(self):
        """
        Create notification configuration and notification configuration variables from the selected Theme.
        It uses the NotificationConfigurationService class for creating the notifications.
        
        Returns:
            bool: Return True to indicate everything went fine.
        """
        notification_configuration_service = NotificationConfigurationService()

        for theme_notification_configuration in ThemeNotificationConfiguration.theme_.theme_notification_configurations_by_theme_id(self.theme.id):

            theme_notification_variables = ThemeNotificationConfigurationVariable.theme_.theme_notification_configuration_variables_by_notification_configuration_id_ordered(
                theme_notification_configuration.id
            )
            for theme_notification_variable in theme_notification_variables:
                notification_configuration_service.add_notification_variable(self.theme_reference.get_field_reference(theme_notification_variable.field.id).id)
            
            notification_configuration_service.save_notification_configuration(
                company_id=self.company_id, 
                user_id=self.user_id,
                for_company=theme_notification_configuration.for_company,
                name=theme_notification_configuration.name,
                text=theme_notification_configuration.text,
                days_diff=theme_notification_configuration.days_diff,
                form=self.theme_reference.get_formulary_reference(theme_notification_configuration.form.id),
                field=self.theme_reference.get_field_reference(theme_notification_configuration.field.id)
            )

        return True

    def __create_dashboard(self):
        """
        Create dashboard chart configuration from the selected Theme.
        It uses the DashboardChartConfigurationService class for creating the dashboard charts, that's because
        we need to validate the billing when inserting.
        
        Returns:
            bool: Return True to indicate everything went fine.
        """
        for theme_dashboard_chart_configuration in ThemeDashboardChartConfiguration.theme_.theme_dashboard_chart_configuration_by_theme_id_ordered(self.theme.id):
            dashboard_chart_configuration_service = DashboardChartConfigurationService(
                self.company_id, 
                self.user_id, 
                self.theme_reference.get_formulary_reference(theme_dashboard_chart_configuration.form.id)
            )
            dashboard_chart_configuration_service.create_or_update(
                name=theme_dashboard_chart_configuration.name,
                for_company=theme_dashboard_chart_configuration.for_company,
                value_field=self.theme_reference.get_field_reference(theme_dashboard_chart_configuration.value_field.id),
                label_field=self.theme_reference.get_field_reference(theme_dashboard_chart_configuration.label_field.id),
                number_format_type=theme_dashboard_chart_configuration.number_format_type,
                chart_type=theme_dashboard_chart_configuration.chart_type,
                aggregation_type=theme_dashboard_chart_configuration.aggregation_type
            )
        return True

    @transaction.atomic
    def select(self):
        """
        This is activated and used when the user clicks the `use` button for selecting a theme.
        It takes a template id and uses it to build the actual data the user will be using for the company
        of the user.

        Returns:
            bool: returns True to indicate that everything was created
        """
        group = self.__create_group()
        self.__create_forms(group)
        self.__create_sections()
        self.__create_fields()

        self.__create_kanban()
        self.__create_notification()
        self.__create_dashboard()
        return True