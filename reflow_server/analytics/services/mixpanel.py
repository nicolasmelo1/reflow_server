from reflow_server.data.managers import form
from django.conf import settings

from reflow_server.authentication.models import UserExtended

from mixpanel import Mixpanel


class MixpanelService:
    def __init__(self):
        """
        Everything that is mixpanel related should be defined here not in the code itself.

        For reference you can use this documentation: https://developer.mixpanel.com/docs/what-is-mixpanel
        Also, for python you can use: 
        And if you need to set up the API directly use this: https://developer.mixpanel.com/v2.51/reference/overview
        """
        self.mixpanel = Mixpanel(settings.MIXPANEL_TOKEN)
    # ------------------------------------------------------------------------------------------
    def dispatch_event(self, event_name, event_data):
        """
        This is responsible for dispatching the events to each handler so we can send more data if needed
        we can group together events and so on. The handlers will be similar to 'AnalyticsEvent' with the only difference
        the methods will have the 'track_' keyword in front of the method name.

        Args:
            event_name (str): The name of the event, usually those will be defined in 'EVENTS' variable in the
                              'settings.py' file
            event_data (dict): The data of the event, check `data_parameters` for reference on what keys does
                               the dict contains.

        Returns:
            bool: Returns True if there was a handler for this event, and False if not, this will probably
                  doesn't change a thing for who is calling this method, but might be nice for tracking or debugging
                  purposes
        """
        handler = getattr(self, 'track_%s' % event_name, None)
        if handler:
            self.create_or_update_user_profile(event_data.get('user_id'))
            handler(**event_data)
            return True
        else:
            return False
    # ------------------------------------------------------------------------------------------
    def create_or_update_user_profile(self, user_id=None):
        """
        Every user that we have in our platform should be also saved inside of mixpanel
        this way the end user that uses mixpanel can see more information about the user in each event.

        Args:
            user_id: The id of the user you want to save on mixpanel
        """
        if user_id:
            user = UserExtended.objects.filter(id=user_id).first()
            if user:
                self.mixpanel.people_set(user_id, {
                    '$first_name'    : user.first_name,
                    '$last_name'     : user.last_name,
                    '$email'         : user.email
                })
    # ------------------------------------------------------------------------------------------
    def track_user_onboarding(self, user_id, company_id):
        self.mixpanel.track(user_id, 'User Onboarding', {
            'company_id': company_id
        })
    # ------------------------------------------------------------------------------------------
    def track_user_login(self, user_id, company_id):
        self.mixpanel.track(user_id, 'User Login', {
            'company_id': company_id
        })
    # ------------------------------------------------------------------------------------------
    def track_user_refresh_token(self, user_id, company_id):
        self.handle_user_login(user_id, company_id)
    # ------------------------------------------------------------------------------------------
    def track_formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public):
        self.mixpanel.track(user_id, 'Formulary Record Created', {
            'company_id': company_id,
            'form_id': form_id,
            'form_record_id': form_data_id,
            'is_public': is_public
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_data_udated(self, user_id, company_id, form_id, form_data_id, is_public):
        self.mixpanel.track(user_id, 'Formulary Record Updated', {
            'company_id': company_id,
            'form_id': form_id,
            'form_record_id': form_data_id,
            'is_public': is_public
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_created(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Formulary Created', {
            'company_id': company_id,
            'form_id': form_id
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_updated(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Formulary Updated', {
            'company_id': company_id,
            'form_id': form_id
        })
    # ------------------------------------------------------------------------------------------
    def track_new_paying_company(self, user_id, company_id, total_paying_value):
        self.mixpanel.track(user_id, 'Company Started Paying', {
            'company_id': company_id,
            'total_paying_value': total_paying_value
        })
    # ------------------------------------------------------------------------------------------
    def track_updated_billing_information(self, user_id, company_id, total_paying_value):
        self.mixpanel.track('Company Updated Billing Information', {
            'user_id': user_id,
            'company_id': company_id,
            'total_paying_value': total_paying_value
        })
    # ------------------------------------------------------------------------------------------
    def track_field_created(self, user_id, company_id, form_id, section_id, field_id):
        self.track_formulary_updated(user_id, company_id, form_id)
    # ------------------------------------------------------------------------------------------
    def track_field_updated(self, user_id, company_id, form_id, section_id, field_id):
        self.track_formulary_updated(user_id, company_id, form_id)
    # ------------------------------------------------------------------------------------------
    def track_theme_select(self, user_id, company_id, theme_id):
        self.mixpanel.track(user_id, 'Selected Theme', {
            'company_id': company_id,
            'theme_id': theme_id
        })
    # ------------------------------------------------------------------------------------------
    def track_theme_eyeballing(self, user_id, theme_id):
        if user_id:
            self.mixpanel.track(user_id, 'Eyeballing Theme', {
                'theme_id': theme_id
            })
    # ------------------------------------------------------------------------------------------
    def track_pdf_template_downloaded(self, user_id, company_id, form_id, pdf_template_id):
        self.mixpanel.track(user_id, 'PDF Downloaded', {
            'company_id': company_id,
            'form_id': form_id,
            'pdf_template_id': pdf_template_id
        })
    # ------------------------------------------------------------------------------------------
    def track_pdf_template_updated(self, user_id, company_id, form_id, pdf_template_id):
        self.mixpanel.track(user_id, 'PDF Template Updated', {
            'company_id': company_id,
            'form_id': form_id,
            'pdf_template_id': pdf_template_id
        })
    # ------------------------------------------------------------------------------------------
    def track_pdf_template_created(self, user_id, company_id, form_id, pdf_template_id):
        self.track_pdf_template_updated(user_id, company_id, form_id, pdf_template_id)
    # ------------------------------------------------------------------------------------------
    def track_kanban_default_settings_updated(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        self.mixpanel.track(user_id, 'Kanban Obligatory Settings Updated', {
            'company_id': company_id,
            'form_id': form_id,
            'kanban_card_id': kanban_card_id,
            'kanban_dimension_id': kanban_dimension_id
        })
    # ------------------------------------------------------------------------------------------
    def track_kanban_default_settings_created(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        self.track_kanban_default_settings_updated(user_id, company_id, form_id, kanban_card_id, kanban_dimension_id)
    # ------------------------------------------------------------------------------------------
    def track_kanban_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Kanban Eyeballing', {
            'company_id': company_id,
            'form_id': form_id
        })
    # ------------------------------------------------------------------------------------------
    def track_listing_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Listing Eyeballing', {
            'company_id': company_id,
            'form_id': form_id
        })
    # ------------------------------------------------------------------------------------------
    def track_dashboard_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Dashboard Eyeballing', {
            'company_id': company_id,
            'form_id': form_id
        })
    # ------------------------------------------------------------------------------------------
    def track_notification_loaded(self, user_id, company_id):
        self.mixpanel.track(user_id, 'Notification Eyeballing', {
            'company_id': company_id
        })
    # ------------------------------------------------------------------------------------------
