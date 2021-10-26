from reflow_server.analytics.services import AnalyticsService


class AnalyticsEvents:
    def __init__(self):
        """
        This event is used to track everything users do in our plataform, since it's on the analytics app
        the idea is that everything the user does in our platform that is trackable and generates an Event should
        be tracked here by the analytics event.

        This way we can make queries to track everything that happens inside of our platform.
        """
        self.analytics_service = AnalyticsService()
    # ------------------------------------------------------------------------------------------
    def user_started_onboarding(self, visitor_id):
        """
        This event is fired whenever a user starts filling the onboarding. This is only fired if the user has a visitor_id, otherwise
        it doesn't fire.

        Args:
            visitor_id (str): This is a reflow_visitor_id that is defined in reflow_tracking application that tracks
                              the user before he is a user of reflow, so check it before everything
        """
        if visitor_id:
            self.analytics_service.register_event('user_started_onboarding', 
                visitor_id=visitor_id
            )
    # ------------------------------------------------------------------------------------------
    def user_onboarding(self, user_id, company_id, visitor_id):
        """
        This event is fired whenever a new user finishes the onboarding.

        Args:
            user_id (int): A UserExtended instance id.
            company_id (int): A Company instance id.
            visitor_id (str): This is a reflow_visitor_id that is defined in reflow_tracking application that tracks
                              the user before he is a user of reflow, so check itbefore everything
        """
        self.analytics_service.register_event('user_onboarding', 
            user_id=user_id, 
            company_id=company_id,
            visitor_id=visitor_id
        )
    # ------------------------------------------------------------------------------------------
    def user_login(self, user_id, company_id):
        """
        THis event is fired whenever the user login in the platform.

        Args:
            user_id (int): The UserExtended instance id of the user that just login
            company_id (int): The company where the user login.
        """
        self.analytics_service.register_event('user_login', 
            user_id=user_id, 
            company_id=company_id
        )
    # ------------------------------------------------------------------------------------------
    def user_refresh_token(self, user_id, company_id):
        """
        This event is fired whenever the user requests a new refresh_token, this is needed so we count
        it as a login since the user stay logged as long as needed.

        Args:
            user_id (int): The UserExtended instance id of the user we just sent the new token to
            company_id (int): The Company instance id, this might change in the near future and this might not be tracked.
        """
        self.analytics_service.register_event('user_refresh_token', 
            user_id=user_id, 
            company_id=company_id
        )
    # ------------------------------------------------------------------------------------------
    def user_created(self, user_id, company_id):
        """
        This event is fired when a new user is added to a company.

        Args:
            user_id (int): The id of the user that was added.
            company_id (int): The id of the company where the user was added.
        """
        self.analytics_service.register_event('user_created', 
            company_id=company_id,
            user_id=user_id
        )
    # ------------------------------------------------------------------------------------------
    def user_updated(self, user_id, company_id):
        """
        This event is fired when a user is updated.

        Args:
            user_id (int): The UserExtended instance id of the user that was updated.
            company_id (int): The Company instance id on what company does this user was updated. 
        """
        self.analytics_service.register_event('user_updated', 
            user_id=user_id, 
            company_id=company_id
        )
    # ------------------------------------------------------------------------------------------
    def formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public, data):
        """
        This event is fired when the a new record is created in the formulary. So the formulary is created but when we add
        new data to it.

        Args:
            user_id (int): The UserExtended instance id of the user. This is the user that added new data. Remember that public
                           formulary also has the id of the user, so we have the 'is_public' to know that it is a public formulary.
            company_id (int): The Company instance id on what company does this formulary data was added. 
            form_id (int): The Form instance id, on what formulary this data was added. 
            form_data_id (int): What was the data added. 
            is_public (bool): Is it a public formulary or not?
        """
        self.analytics_service.register_event('formulary_data_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            form_data_id=form_data_id,
            is_public=is_public
        )
    # ------------------------------------------------------------------------------------------
    def formulary_data_updated(self, user_id, company_id, form_id, form_data_id, is_public, data):
        """
        Similar to `.formulary_data_created()` except it works when the data was updated in a formulary.

        Args:
            user_id (int): The UserExtended instance id of the user. This is the user that updated the data. Remember that public
                           formulary also has the id of the user, so we have the 'is_public' to know that it is a public formulary.
            company_id (int): The Company instance id on what company does this formulary data was updated. 
            form_id (int): The Form instance id, on what formulary this data was updated. 
            form_data_id (int): What was the data updated. 
            is_public (bool): Is it a public formulary or not?
        """
        self.analytics_service.register_event('formulary_data_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            form_data_id=form_data_id,
            is_public=is_public
        )
    # ------------------------------------------------------------------------------------------
    def formulary_created(self, user_id, company_id, form_id):
        """
        A new formulary/page was created by a user and for a company.

        Args:
            user_id (int): The id of the user that created the formulary.
            company_id (int): The id of the company where this form/page was created.
            form_id (int): The id of the page/form that was created
        """
        self.analytics_service.register_event('formulary_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id
        )
    # ------------------------------------------------------------------------------------------
    def formulary_updated(self, user_id, company_id, form_id):
        """
        When the user updates a formulary/page we fire this event. Can be by changing it's name, eanbling, or not.

         Args:
            user_id (int): The id of the user that updated the formulary.
            company_id (int): The id of the company where this form/page was updated.
            form_id (int): The id of the page/form that was updated
        """
        self.analytics_service.register_event('formulary_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id
        )
    # ------------------------------------------------------------------------------------------
    def field_created(self, user_id, company_id, form_id, section_id, field_id):
        """
        If a field was created by a user we fire this event.

        Args:
            user_id (int): The user that updated the field.
            company_id (int): The Company instance id that updated the field.
            form_id (int): The Form instance id of where the field was updated.
            section_id (int): The Section instance id of where the field was created also.
            field_id (int): The Field instance id that was created.
        """
        self.analytics_service.register_event('field_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            section_id=section_id,
            field_id=field_id
        )  
    # ------------------------------------------------------------------------------------------
    def field_updated(self, user_id, company_id, form_id, section_id, field_id):
        """
        If a field was updated by a user we fire this event.

        Args:
            user_id (int): The user that updated the field.
            company_id (int): The Company instance id that updated the field.
            form_id (int): The Form instance id of where the field was updated.
            section_id (int): The Section instance id of where the field was updated also.
            field_id (int): The Field instance id that was updated.
        """
        self.analytics_service.register_event('field_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            section_id=section_id,
            field_id=field_id
        )  
    # ------------------------------------------------------------------------------------------
    def new_paying_company(self, user_id, company_id, total_paying_value):
        """
        A company started paying.

        Args:
            user_id (int): The user that changed the billing information.
            company_id (int): The company that started paying.
            total_paying_value (float): The value of the user that started paying.
        """
        self.analytics_service.register_event('new_paying_company', 
            user_id=user_id,
            company_id=company_id,
            total_paying_value=total_paying_value
        )
    # ------------------------------------------------------------------------------------------
    def updated_billing_information(self, user_id, company_id, total_paying_value):
        """
        A company updated a billing information.

        Args:
            user_id (int): The user that changed the billing information.
            company_id (int): The company that started paying.
            total_paying_value (float): The value of the user that started paying.
        """
        self.analytics_service.register_event('updated_billing_information',
            user_id=user_id,
            company_id=company_id,
            total_paying_value=total_paying_value
        )
    # ------------------------------------------------------------------------------------------
    def removed_old_draft(self, user_id, company_id, draft_id, draft_is_public):
        """
        When the worker removes an old draft from the database.

        Args:
            user_id (int): The user instance id.
            company_id (int): The company of where the draft was removed.
            draft_id (int): The draft id that was removed.
            draft_is_public (bool): If a public user has added a draft defines if the draft removes was a public draft (for anonymous users).
        """
        self.analytics_service.register_event('removed_old_draft', 
            user_id=user_id,
            company_id=company_id,
            draft_id=draft_id,
            draft_is_public=draft_is_public
        )
    # ------------------------------------------------------------------------------------------
    def company_information_updated(self, user_id, company_id):
        """
        If the information of a company was updated we fire this event.

        Args:
            user_id (int): The id of the user that updated the company information.
            company_id (int): The id of the company that updated its information.
        """
        self.analytics_service.register_event('company_information_updated', 
            company_id=company_id,
            user_id=user_id
        )
    # ------------------------------------------------------------------------------------------
    def theme_select(self, user_id, company_id, theme_id):
        """
        If a theme was selected we fire this event.

        Args:
            user_id (int): The id of the user that selected the theme.
            company_id (int): The company that selected the theme.
            theme_id (int): The id of the theme that was selected.
        """
        self.analytics_service.register_event('theme_select', 
            company_id=company_id,
            user_id=user_id,
            theme_id=theme_id
        )
    # ------------------------------------------------------------------------------------------
    def theme_eyeballing(self, user_id, theme_id):
        """
        The theme is being eyeballed. This means the user is seeing a template.

        Args:
            user_id ([None, int]): The id of the user that is eyeballing a template
            theme_id (int): The id of the template that is being eyeballed.
        """
        self.analytics_service.register_event('theme_eyeballing', 
            user_id=user_id,
            theme_id=theme_id
        )
    # ------------------------------------------------------------------------------------------
    def pdf_template_downloaded(self, user_id, company_id, form_id, pdf_template_id):
        """
        A PDF Generator template was downloaded. This means a PDF was downloaded.

        Args:
            user_id (int): The User instance that is downloading the PDF template.
            company_id (int): The Company instance id that was downloaded.
            form_id (int): The Form instance of the PDF Template, from what formulary the PDF Template was on.
            pdf_template_id (int): The PDFGenerator instance id.
        """
        self.analytics_service.register_event('pdf_template_downloaded', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )
    # ------------------------------------------------------------------------------------------
    def pdf_template_created(self, user_id, company_id, form_id, pdf_template_id):
        """
        A New PDF Template was created.

        Args:
            user_id (int): The User that created the PDF Template
            company_id (int): On what Company this PDF Template was created.
            form_id (int): On what formulary does this PDF template was created.
            pdf_template_id (int): The PDF Template instance that was created.
        """
        self.analytics_service.register_event('pdf_template_created', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )
    # ------------------------------------------------------------------------------------------
    def pdf_template_updated(self, user_id, company_id, form_id, pdf_template_id):
        """
        A PDF Template was updated.

        Args:
            user_id (int): The User that updated the PDF Template
            company_id (int): On what Company this PDF Template was updated.
            form_id (int): On what formulary does this PDF template was updated.
            pdf_template_id (int): The PDF Template instance that was updated.
        """
        self.analytics_service.register_event('pdf_template_updated', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )
    # ------------------------------------------------------------------------------------------
    def kanban_default_settings_created(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        """
        When the default settings of a kanban was created. Was set. We fire this event. This means that if this is not fired
        the user hasn't set the default configuration to use the kanban. So, in other words, the user is not using the kanban or it
        is having a difficult time chaging the kanban configuration.

        Args:
            user_id (int): The User id that set the default kanban setting for a particular formulary
            company_id (int): For what company did the user set the default kanban setting.
            form_id (int): For what formulary/page did the user set the default kanban setting
            kanban_card_id (int): The default card selected when loading the kanban view for this user.
            kanban_dimension_id (int): The default dimension selected when loading the kanban view for this user.
        """
        self.analytics_service.register_event('kanban_default_settings_created', 
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id, 
            kanban_card_id=kanban_card_id, 
            kanban_dimension_id=kanban_dimension_id
        )
    # ------------------------------------------------------------------------------------------
    def kanban_default_settings_updated(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        """
        Similar to `.kanban_default_settings_created()` event but this is fired when the settings was updated, not when it was created.

        Args:
            user_id (int): The User id that set the default kanban setting for a particular formulary
            company_id (int): For what company did the user set the default kanban setting.
            form_id (int): For what formulary/page did the user set the default kanban setting
            kanban_card_id (int): The default card selected when loading the kanban view for this user.
            kanban_dimension_id (int): The default dimension selected when loading the kanban view for this user.
        """
        self.analytics_service.register_event('kanban_default_settings_updated', 
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id, 
            kanban_card_id=kanban_card_id, 
            kanban_dimension_id=kanban_dimension_id
        )
    # ------------------------------------------------------------------------------------------
    def kanban_loaded(self, user_id, company_id, form_id):
        """
        The kanban was loaded to the user, so this means the user is eyeballing the kanban page when this is fired.

        Args:
            user_id (int): The UserExtended instance that was eyeballing the kanban
            company_id (int): The Company instance where the user was eyeballing the kanban on
            form_id (int): The Formulary/page instance where the user was eyeballing the kanban.
        """
        self.analytics_service.register_event('kanban_loaded',
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id
        )
    # ------------------------------------------------------------------------------------------
    def listing_loaded(self, user_id, company_id, form_id):
        """
        The listing was loaded to the user, so the user uis eyeballing the listing page when this event is fired.

        Args:
            user_id (int): The UserExtended instance that was eyeballing the listing
            company_id (int): The Company instance where the user was eyeballing the listing on
            form_id (int): The Formulary/page instance where the user was eyeballing the listing.
        """
        self.analytics_service.register_event('listing_loaded',
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id
        )
    # ------------------------------------------------------------------------------------------
    def dashboard_loaded(self, user_id, company_id, form_id):
        """
        The dashboard was loaded to the user, so the user uis eyeballing the dashboard page when this event is fired.

        Args:
            user_id (int): The UserExtended instance that was eyeballing the dashboard
            company_id (int): The Company instance where the user was eyeballing the dashboard on
            form_id (int): The Formulary/page instance where the user was eyeballing the dashboard.
        """
        self.analytics_service.register_event('dashboard_loaded',
            user_id=user_id,
            company_id=company_id,
            form_id=form_id
        )
    # ------------------------------------------------------------------------------------------
    def dashboard_chart_created(self, user_id, company_id, form_id, dashboard_chart_id):
        self.analytics_service.register_event('dashboard_chart_created',
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            dashboard_chart_id=dashboard_chart_id
        )
    # ------------------------------------------------------------------------------------------
    def dashboard_chart_updated(self, user_id, company_id, form_id, dashboard_chart_id):
        self.analytics_service.register_event('dashboard_chart_updated',
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            dashboard_chart_id=dashboard_chart_id
        )
    # ------------------------------------------------------------------------------------------
    def notification_loaded(self, user_id, company_id):
        """
        The notification was loaded to the user, so the user uis eyeballing the notification page when this event is fired.

        Args:
            user_id (int): The UserExtended instance that was eyeballing the notification
            company_id (int): The Company instance where the user was eyeballing the notification on
        """
        self.analytics_service.register_event('notification_loaded', 
            user_id=user_id,
            company_id=company_id
        )
    # ------------------------------------------------------------------------------------------
    def notification_configuration_created(self, user_id, company_id, form_id, notification_configuration_id):
        self.analytics_service.register_event('notification_configuration_created',
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            notification_configuration_id=notification_configuration_id
        )
    # ------------------------------------------------------------------------------------------
    def notification_configuration_updated(self, user_id, company_id, form_id, notification_configuration_id):
        self.analytics_service.register_event('notification_configuration_updated',
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            notification_configuration_id=notification_configuration_id
        )
    # ------------------------------------------------------------------------------------------
