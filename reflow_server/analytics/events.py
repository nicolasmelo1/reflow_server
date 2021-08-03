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

    def user_onboarding(self, user_id, company_id):
        """
        This event is fired whenever a new user finishes the onboarding.

        Args:
            user_id (int): A UserExtended instance id.
            company_id (int): A Company instance id.
        """
        self.analytics_service.register_event('user_onboarding', 
            user_id=user_id, 
            company_id=company_id
        )

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

    def formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public):
        self.analytics_service.register_event('formulary_data_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            form_data_id=form_data_id,
            is_public=is_public
        )
        
    def formulary_data_updated(self, user_id, company_id, form_id, form_data_id, is_public):
        self.analytics_service.register_event('formulary_data_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            form_data_id=form_data_id,
            is_public=is_public
        )
    
    def formulary_created(self, user_id, company_id, form_id):
        self.analytics_service.register_event('formulary_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id
        )    

    def formulary_updated(self, user_id, company_id, form_id):
        self.analytics_service.register_event('formulary_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id
        )    

    def field_created(self, user_id, company_id, form_id, section_id, field_id):
        self.analytics_service.register_event('field_created', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            section_id=section_id,
            field_id=field_id
        )  

    def field_updated(self, user_id, company_id, form_id, section_id, field_id):
        self.analytics_service.register_event('field_updated', 
            user_id=user_id, 
            company_id=company_id,
            form_id=form_id,
            section_id=section_id,
            field_id=field_id
        )  
        
    def new_paying_company(self, user_id, company_id, total_paying_value):
        self.analytics_service.register_event('new_paying_company', 
            user_id=user_id,
            company_id=company_id,
            total_paying_value=total_paying_value
        )
    
    def updated_billing_information(self, user_id, company_id, total_paying_value):
        self.analytics_service.register_event('updated_billing_information',
            user_id=user_id,
            company_id=company_id,
            total_paying_value=total_paying_value
        )

    def removed_old_draft(self, company_id, draft_id, draft_is_public):
        self.analytics_service.register_event('removed_old_draft', 
            company_id=company_id,
            draft_id=draft_id,
            draft_is_public=draft_is_public
        )

    def company_information_updated(self, user_id, company_id):
        self.analytics_service.register_event('company_information_updated', 
            company_id=company_id,
            user_id=user_id
        )

    def theme_select(self, user_id, company_id, theme_id):
        self.analytics_service.register_event('theme_select', 
            company_id=company_id,
            user_id=user_id,
            theme_id=theme_id
        )

    def theme_eyeballing(self, theme_id):
        self.analytics_service.register_event('theme_eyeballing', 
            theme_id=theme_id
        )

    def pdf_template_downloaded(self, user_id, company_id, form_id, pdf_template_id):
        self.analytics_service.register_event('pdf_template_downloaded', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )

    def pdf_template_created(self, user_id, company_id, form_id, pdf_template_id):
        self.analytics_service.register_event('pdf_template_created', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )

    def pdf_template_updated(self, user_id, company_id, form_id, pdf_template_id):
        self.analytics_service.register_event('pdf_template_updated', 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id,
            pdf_template_id=pdf_template_id
        )

    def kanban_default_settings_created(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        self.analytics_service.register_event('kanban_default_settings_created', 
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id, 
            kanban_card_id=kanban_card_id, 
            kanban_dimension_id=kanban_dimension_id
        )

    def kanban_default_settings_updated(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        self.analytics_service.register_event('kanban_default_settings_updated', 
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id, 
            kanban_card_id=kanban_card_id, 
            kanban_dimension_id=kanban_dimension_id
        )

    def kanban_loaded(self, user_id, company_id, form_id):
        self.analytics_service.register_event('kanban_loaded',
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id
        )

    def listing_loaded(self, user_id, company_id, form_id):
        self.analytics_service.register_event('listing_loaded',
            user_id=user_id, 
            company_id=company_id, 
            form_id=form_id
        )
