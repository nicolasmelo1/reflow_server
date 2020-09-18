from django.db import transaction

from reflow_server.theme.models import Theme, ThemeForm, ThemeField, ThemeFieldOptions, \
    ThemeKanbanDimensionOrder, ThemeKanbanCard, ThemeKanbanCardField, \
    ThemeNotificationConfiguration, ThemeNotificationConfigurationVariable, \
    ThemeDashboardChartConfiguration
from reflow_server.authentication.models import UserExtended
from reflow_server.kanban.models import KanbanDimensionOrder

from reflow_server.formulary.services.group import GroupService
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService
from reflow_server.kanban.services import KanbanCardService, KanbanService
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService


class ThemeSelectService:
    def __init__(self, theme_id, company_id, user_id):
        self.theme = Theme.theme_.theme_by_theme_id(theme_id)
        self.company_users = UserExtended.theme_.users_active_by_company_id(company_id)
        self.company_id = company_id
        self.user_id = user_id
        
    def __create_group(self):
        """
        Creates the group. It's important to notice that groups have the company_type name on it 
        and not the theme name. So if this theme is on the section `Sales` and the name of the theme is
        `Sales for Startups`. The name will be `Sales` and NOT `Sales for startups`

        Returns:
            reflow_server.formulary.models.Group: The newly created group instance that will holds all of the formularies
            created of this template/theme.
        """
        group_service = GroupService(self.company_id)
        return group_service.create_group(self.theme.company_type.label_name)

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
            dict: This is a dict that holds the reference of ThemeForm and Form instances.
                  On this dict, each key is the ThemeForm id, and the value is each Form 
                  instance created. This way whenever we encounter a ThemeForm we can get 
                  the Form instance it references to.
        """
        # this contains the reference on what the themeform id was as key and the created Form instance as the value.
        # this way we can know the actual relation of the theme_form_id.
        formulary_reference = {}

        formulary_service = FormularyService(self.user_id, self.company_id)

        for theme_form in ThemeForm.theme_.main_theme_forms_by_theme_id(self.theme.id):
            formulary_instance = formulary_service.save_formulary(True, theme_form.label_name, theme_form.order, group)
            formulary_reference[theme_form.id] = formulary_instance

        return formulary_reference

    def __create_sections(self, formulary_reference):
        """
        This creates sections of the ThemeForm instances that have depends_on as not null.
        We use the SectionService for creating sections so it can handle most of the logic.

        There are two things important to understand:
        - `formulary_reference` dict is also updated with the sections, SO the `formulary_reference`
        holds the reference on ThemeForm instances, we DO NOT separate between sections and forms.
        - When the section has a conditional, we can't set the conditiona_on_field yet because we 
        haven't created the field just yet. Because of this we create a reference so after we added the 
        fields we can just add the proper conditionals. Each key of the dict is the field_id the conditional 
        references to and the value is the section instance to update.

        Args:
            formulary_reference (dict): This is a dict that holds the reference of ThemeForm and Form instances.
                                        On this dict, each key is the ThemeForm id, and the value is each Form 
                                        instance created. This way whenever we encounter a ThemeForm we can get 
                                        the Form instance it references to.

        Returns:
            tuple(dict, dict): returns two dicts in a tuple. The first element of this tuple is the formulary_reference
            dict we recieve as parameter but updated with sections also. The second element of this tuple is the 
            `section_conditionals_reference` which is a dict that holds the reference of conditionals for sections.
        """
        section_conditionals_reference = {}

        for theme_section in ThemeForm.theme_.sections_theme_forms_by_theme_id(self.theme.id):
            section_service = SectionService(user_id=self.user_id, company_id=self.company_id, form_id=formulary_reference[theme_section.depends_on.id].id)
                
            section = section_service.save_section(
                True, theme_section.label_name, theme_section.order, 
                theme_section.conditional_value, theme_section.type,
                theme_section.conditional_type, None
            )
            formulary_reference[theme_section.id] = section
            if theme_section.conditional_on_field:
                section_conditionals_reference[theme_section.conditional_on_field.id] = section
        return formulary_reference, section_conditionals_reference
    
    def __create_fields(self, formulary_reference, section_conditionals_reference):
        """
        This method is responsible for creating fields of all of the formularies and sections of a theme.
        
        - First when we create a `form` field type, so a field_type that references to a field of another form,
        we DO NOT create the reference right away. We need to wait the creation of all of the field. THEN we can
        add the specific references.
        - Second, conditionals are bound to a specific field. Like the first item, we also wait the creation of EVERY
        field to add the conditional fields. That's why we use the `section_conditionals_reference` parameter to.

        Last but not least, after all of the fields have been created we return a dict to be used as reference. With this
        we can know by the ThemeField id what Field should we use when we create a new data.
        For example, on NotificationConfigurations (not the Theme ones), they are usually bound to a Field instance.
        ThemeNotificationConfiguration holds the reference for a ThemeField. When we are creating a new NotificationConfiguration
        for the user based on the ThemeNotificationConfiguration we will have initally the ThemeField id. We use this
        to set the correct reference to it.

        Args:
            formulary_reference (dict): This is a dict that holds the reference of ThemeForm and Form instances.
                                        On this dict, each key is the ThemeForm id, and the value is each Form 
                                        instance created. This way whenever we encounter a ThemeForm we can get 
                                        the Form instance it references to.
            section_conditionals_reference (dict): Same as `formulary_reference` except that is just holds sections
                                                   (so instances when depends_on IS NOT NULL). These sections are 
                                                   the ones that have a conditional bound
            to it. The sections with conditional_on_field = None ARE NOT on this dict.

        Returns:
            dict: return a dict to be used as reference. With this we can know by the ThemeField id what Field 
            should we use when we create a new data. On this dict, each key is the ThemeField id, and the value 
            is each Field instance created. This way whenever we encounter a ThemeField we can get the Field 
            instance it references to.
        """
        field_reference = {}
        form_field_as_option_reference = {}
        form_field_type_fields = []

        for theme_field in ThemeField.theme_.theme_fields_by_theme_id(self.theme.id):
            field_options = []

            # if the field is of type `option` or `multi_option` we get the options of the theme to add on the field.
            # initially the `field_options` variable is just an empty list, but if it is from both types we use the
            # options saved.
            if theme_field.type.type in ['option', 'multi_option']:
                field_options = list(ThemeFieldOptions.theme_.options_by_theme_field_id(theme_field_id=theme_field.id))
            
            field_service = FieldService(
                user_id=self.user_id, company_id=self.company_id, form_id=formulary_reference[theme_field.form.depends_on.id].id
            )

            field = field_service.save_field(
                True, theme_field.label_name, theme_field.order, theme_field.is_unique, theme_field.field_is_hidden, 
                theme_field.label_is_hidden, theme_field.placeholder, theme_field.required, formulary_reference[theme_field.form_id],
                None, theme_field.formula_configuration, theme_field.date_configuration_auto_create, theme_field.date_configuration_auto_update,
                theme_field.number_configuration_number_format_type, theme_field.date_configuration_date_format_type, 
                theme_field.period_configuration_period_interval_type, theme_field.type, field_options
            )

            field_reference[theme_field.id] = field

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

                
        # set conditionals on sections
        for theme_field_id, section in section_conditionals_reference.items():
            section.conditional_on_field_id = field_reference[theme_field_id].id
            section.save()

        # set form_field_as_option on fields
        for theme_field in form_field_type_fields:
            field = form_field_as_option_reference[theme_field.id]
            field.form_field_as_option_id = field_reference[theme_field.form_field_as_option_id].id
            field.save()

        return field_reference

    def __create_kanban(self, field_reference):
        """
        Create the kanban dimnesion order values for all of the users of the company and also creates
        the KanbanCard for all of the users.
        This method defines kanban defaults so when the user opens the kanban we can already know its 
        default kanban card and also the default kanban dimension.

        Args:
            field_reference (dict): This is a dict that holds the reference of ThemeField and Field instances.
                                    On this dict, each key is the ThemeField id, and the value is each Field 
                                    instance created. This way whenever we encounter a ThemeField we can get 
                                    the Field instance it references to.

        Returns:
            bool: Return True to indicate everything went fine.
        """
        theme_kanban_dimension_orders = ThemeKanbanDimensionOrder.theme_.theme_kanban_dimension_order_by_theme_id_ordered(self.theme.id)
        theme_kanban_cards = ThemeKanbanCard.theme_.theme_kanban_cards_by_theme_id(self.theme.id)

        for user in self.company_users:
            kanban_card_service = KanbanCardService(user_id=user.id)

            for theme_kanban_dimension in theme_kanban_dimension_orders:
                KanbanDimensionOrder.theme_.create_kanban_dimension_order(
                    dimension_id=field_reference[theme_kanban_dimension.dimension.id].id,
                    order=theme_kanban_dimension.order, 
                    default=theme_kanban_dimension.default, 
                    user_id=user.id, 
                    options=theme_kanban_dimension.options
                )

            for theme_kanban_card in theme_kanban_cards:
                theme_kanban_card_field_ids = ThemeKanbanCardField.theme_.theme_field_ids_by_theme_kanban_card_id(theme_kanban_card.id)
                kanban_card_field_ids = [field_reference[theme_kanban_card_field_id].id for theme_kanban_card_field_id in theme_kanban_card_field_ids]

                # we create a new kanban card with it's fields, and then we set the default of the instance created
                # to be equal the theme_kanban_card default
                kanban_card_instance = kanban_card_service.save_kanban_card(kanban_card_field_ids)
                kanban_card_instance.default = theme_kanban_card.default
                kanban_card_instance.save()
        return True

    def __create_notification(self, field_reference, formulary_reference):
        """
        Create notification configuration and notification configuration variables from the selected Theme.
        It uses the NotificationConfigurationService class for creating the notifications.

        Args:
            field_reference (dict): This is a dict that holds the reference of ThemeField and Field instances.
            On this dict, each key is the ThemeField id, and the value is each Field instance created. This way
            whenever we encounter a ThemeField we can get the Field instance it references to.
            formulary_reference (dict): This is a dict that holds the reference of ThemeForm and Form instances.
            On this dict, each key is the ThemeForm id, and the value is each Form instance created. This way
            whenever we encounter a ThemeForm we can get the Form instance it references to.

        Returns:
            bool: Return True to indicate everything went fine.
        """
        notification_configuration_service = NotificationConfigurationService()

        for theme_notification_configuration in ThemeNotificationConfiguration.theme_.theme_notification_configurations_by_theme_id(self.theme.id):

            theme_notification_variables = ThemeNotificationConfigurationVariable.theme_.theme_notification_configuration_variables_by_notification_configuration_id_ordered(
                theme_notification_configuration.id
            )
            for theme_notification_variable in theme_notification_variables:
                notification_configuration_service.add_notification_variable(field_reference[theme_notification_variable.field.id].id)
            
            notification_configuration_service.save_notification_configuration(
                company_id=self.company_id, 
                user_id=self.user_id,
                for_company=theme_notification_configuration.for_company,
                name=theme_notification_configuration.name,
                text=theme_notification_configuration.text,
                days_diff=theme_notification_configuration.days_diff,
                form=formulary_reference[theme_notification_configuration.form.id],
                field=field_reference[theme_notification_configuration.field.id]
            )

        return True

    def __create_dashboard(self, field_reference, formulary_reference):
        pass

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
        formulary_reference = self.__create_forms(group)
        formulary_reference, section_conditionals_reference = self.__create_sections(formulary_reference)
        field_reference = self.__create_fields(formulary_reference, section_conditionals_reference)

        self.__create_kanban(field_reference)
        self.__create_notification(field_reference, formulary_reference)
        return True