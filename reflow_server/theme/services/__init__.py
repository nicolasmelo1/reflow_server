from django.db import transaction

from reflow_server.formulary.models import Group, Form, Field
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.fields import FieldService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.kanban.models import KanbanCard, KanbanDimensionOrder
from reflow_server.kanban.services.kanban_card import KanbanCardService
from reflow_server.authentication.models import UserExtended
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService
from reflow_server.theme.models import ThemeForm, ThemeField, ThemeFieldOptions, \
    ThemeKanbanCard, ThemeKanbanCardField, ThemeNotificationConfiguration, \
    ThemeNotificationConfigurationVariable, ThemeKanbanDimensionOrder


class ThemeService:
    @staticmethod
    @transaction.atomic
    def select_theme(theme, company_id, user_id):
        group_order = Group.objects.filter(company_id=company_id).order_by('-order').values_list('order', flat=True).first()
        group = Group.objects.create(name=theme.company_type.label_name, company_id=company_id, enabled=True, order=group_order+1 if group_order else 1)

        company_users = UserExtended.theme_.users_active_by_company_id(company_id)


        field_reference = dict()
        form_reference = dict()
        notification_configuration_reference = dict()
        kanban_card_reference = dict()
        form_conditionals_reference = dict()
        form_field_as_option_reference = dict()

        saved_field_options = list()
        ######################
        #                    #
        #       FORMS        #
        #                    #
        ######################
        theme_forms = ThemeForm.objects.filter(theme=theme)

        # forms first
        for theme_form in theme_forms.filter(depends_on__isnull=True):
            formulary_service = FormularyService(user_id=user_id, company_id=company_id)
            form = formulary_service.save_formulary(Form(), True, theme_form.label_name, theme_form.order, group)
            form_reference[theme_form.id] = form.id

        # now sections
        for theme_section in theme_forms.filter(depends_on__isnull=False):
            section_service = SectionService(user_id=user_id, company_id=company_id, form_id=form_reference[theme_section.depends_on.id])
            
            section = section_service.save_section(Form(), True, theme_section.label_name, 
            theme_section.order, theme_section.conditional_value, theme_section.type,
            theme_section.conditional_type, None)
            form_reference[theme_section.id] = section.id
            if theme_section.conditional_on_field:
                form_conditionals_reference[theme_section.id] = section
            
        ######################
        #                    #
        #       FIELDS       #
        #                    #
        ######################
        for theme_field in ThemeField.objects.filter(form__in=theme_forms):
            field_options = list(ThemeFieldOptions.objects.filter(field=theme_field).values_list('option', flat=True))

            field_service = FieldService(user_id=user_id, company_id=company_id, form_id=form_reference[theme_field.form.depends_on.id])
            field = field_service.save_field(
                Field(), True, theme_field.label_name, theme_field.order, theme_field.is_unique, theme_field.field_is_hidden, 
                theme_field.label_is_hidden, theme_field.placeholder, theme_field.required, form_reference[theme_field.form_id],
                None, theme_field.formula_configuration, theme_field.date_configuration_auto_create, theme_field.date_configuration_auto_update,
                theme_field.number_configuration_number_format_type, theme_field.date_configuration_date_format_type, 
                theme_field.period_configuration_period_interval_type, theme_field.type, field_options
            )
            field_reference[theme_field.id] = field.id
            if theme_field.form_field_as_option not in (None, ''):
                form_field_as_option_reference[theme_field.id] = field

        
        # set conditionals on forms
        for conditional_section in theme_forms.filter(depends_on__isnull=False, conditional_on_field__isnull=False):
            section = form_conditionals_reference[conditional_section.id]
            section.conditional_on_field_id = field_reference[conditional_section.conditional_on_field_id]
            section.save()

        # set form_field_as_option on fields
        for theme_field in ThemeField.objects.filter(form__in=theme_forms, form_field_as_option__isnull=False):
            field = form_field_as_option_reference[theme_field.id]
            field.form_field_as_option_id = field_reference[theme_field.form_field_as_option_id]
            field.save()

        #######################
        #                     #
        # DATA VISUALIZATIONS #
        #                     #
        #######################              
        # set kanban dimension
        for theme_kanban_dimension in ThemeKanbanDimensionOrder.objects.filter(dimension__form__in=theme_forms, theme=theme):
            KanbanDimensionOrder.objects.bulk_create([KanbanDimensionOrder(
                dimension_id=field_reference[theme_kanban_dimension.dimension.id],
                order=theme_kanban_dimension.order, 
                default=theme_kanban_dimension.default, 
                user=user, 
                options=theme_kanban_dimension.options
            ) for user in company_users])
        
        # kanban_cards are kind of complicated, but not that much, we check the reference to check wheter a kanban_card was created or not
        for user in company_users:
            for theme_kanban_card in ThemeKanbanCard.objects.filter(theme=theme):
                field_ids = [field_reference[theme_kanban_card_field.field.id] for theme_kanban_card_field in ThemeKanbanCardField.objects.filter(kanban_card=theme_kanban_card)]

                kanban_card_service = KanbanCardService(user_id=user.id)
                kanban_card_service.save_kanban_card(KanbanCard(), field_ids)
        
        #######################
        #                     #
        #    NOTIFICTIONS     #
        #                     #
        #######################
        for theme_notification_configuration in ThemeNotificationConfiguration.objects.filter(form__in=theme_forms):
            notification_configuration_service = NotificationConfigurationService()

            notification_variables = ThemeNotificationConfigurationVariable.objects.filter(notification_configuration=theme_notification_configuration).order_by('order')
            for notification_variable in notification_variables:
                notification_configuration_service.add_notification_variable(field_reference[notification_variable.field.id])
            
            notification_configuration_service.save_notification_configuration(
                company_id=company_id, 
                user_id=user_id,
                for_company=theme_notification_configuration.for_company,
                name=theme_notification_configuration.name,
                text=theme_notification_configuration.text,
                days_diff=theme_notification_configuration.days_diff,
                form=form_reference[theme_notification_configuration.form.id],
                field=field_reference[theme_notification_configuration.field.id]
            )
        
        return None