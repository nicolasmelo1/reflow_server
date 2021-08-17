from reflow_server.billing.models import CompanyBilling
from django.conf import settings
from django.utils import timezone

from reflow_server.authentication.models import Company, UserExtended

from mixpanel import Mixpanel

from datetime import timedelta

# Formulary_Updated and field_updated events fire for every type of the user
# this is not ideal for the Analytics user but it is for our logging system.
# To prevent that, whenever both events is fired we set the data to send, after that, set this to false.
# The first key is the user_id, the second is the company_id and the last is the form_id
formulary_was_updated = {}
user_profile_updated = {}
trial_company_ids = set()
paying_company_ids = set()

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

        Because we send the 'formulary_updated' event and 'field_updated' event for every type and iteration of the user
        we use the `formulary_was_updated` global variable so we can prevent to send the 'Formulary Updated' event everytime.

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
            if event_name not in ['formulary_updated', 'field_updated']:
                formulary_was_updated.pop(event_data.get('user_id'), None)
            self.create_or_update_user_profile(event_data.get('user_id', None))
            handler(**event_data)
            return True
        else:
            return False
    # ------------------------------------------------------------------------------------------
    def define_company_type(self, company_id=None):
        if company_id == None:
            return 'lead'
        if company_id in trial_company_ids:
            return 'trial'
        elif company_id in paying_company_ids:
            return 'paying'
        else:
            # the company_id is not in trial_company_ids nor paying_company_ids variable, so let's define what the company is
            company_billing = CompanyBilling.objects.filter(company_id=company_id).first()
            if company_billing:
                is_trial = company_billing.is_paying_company == False and company_billing.is_supercompany == False
                if is_trial:
                    trial_company_ids.add(company_id)
                    return self.define_company_type(company_id)
                else:
                    paying_company_ids.add(company_id)
                    return self.define_company_type(company_id)
            else:
                # the company is not a reflow company
                return self.define_company_type(None)
    # ------------------------------------------------------------------------------------------
    def create_or_update_user_profile(self, user_id=None):
        """
        Every user that we have in our platform should be also saved inside of mixpanel
        this way the end user that uses mixpanel can see more information about the user in each event.

        To prevent to update it everytime we keep in memory that the user was updated.

        Args:
            user_id: The id of the user you want to save on mixpanel
        """
        if user_id != None and user_profile_updated.get(user_id, False) == False:
            user = UserExtended.objects.filter(id=user_id).first()
            if user:
                self.mixpanel.people_set(user_id, {
                    '$first_name'    : user.first_name,
                    '$last_name'     : user.last_name,
                    '$email'         : user.email,
                    '$phone'         : user.phone,
                })
                user_profile_updated[user_id] = True
    # ------------------------------------------------------------------------------------------
    def track_user_started_onboarding(self, visitor_id):
        self.mixpanel.track(visitor_id, 'User Started Onboarding')
    # ------------------------------------------------------------------------------------------
    def track_user_onboarding(self, user_id, company_id, visitor_id):
        self.mixpanel.alias(user_id, visitor_id)
        self.mixpanel.track(user_id, 'User Onboarding', {
            'company_id': company_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_user_login(self, user_id, company_id):
        self.mixpanel.track(user_id, 'User Login', {
            'company_id': company_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_user_refresh_token(self, user_id, company_id):
        self.track_user_login(user_id, company_id)
    # ------------------------------------------------------------------------------------------
    def track_formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public):
        self.mixpanel.track(user_id, 'Formulary Record Created', {
            'company_id': company_id,
            'form_id': form_id,
            'form_record_id': form_data_id,
            'is_public': is_public,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_data_udated(self, user_id, company_id, form_id, form_data_id, is_public):
        self.mixpanel.track(user_id, 'Formulary Record Updated', {
            'company_id': company_id,
            'form_id': form_id,
            'form_record_id': form_data_id,
            'is_public': is_public,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_created(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Formulary Created', {
            'company_id': company_id,
            'form_id': form_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_formulary_updated(self, user_id, company_id, form_id):
        if formulary_was_updated.get(user_id, {}).get(company_id, {}).get(form_id, False) == False:
            self.mixpanel.track(user_id, 'Formulary Updated', {
                'company_id': company_id,
                'form_id': form_id,
                'company_type': self.define_company_type(user_id)
            })
            formulary_was_updated[user_id] = {
                company_id: {
                    form_id: True
                }
            }
    # ------------------------------------------------------------------------------------------
    def track_new_paying_company(self, user_id, company_id, total_paying_value):
        trial_company_ids.remove(company_id)
        paying_company_ids.add(company_id)

        self.mixpanel.track(user_id, 'Company Started Paying', {
            'company_id': company_id,
            'total_paying_value': total_paying_value,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_updated_billing_information(self, user_id, company_id, total_paying_value):
        self.mixpanel.track('Company Updated Billing Information', {
            'user_id': user_id,
            'company_id': company_id,
            'company_type': self.define_company_type(user_id),
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
            'company_type': self.define_company_type(user_id),
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
            'pdf_template_id': pdf_template_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_pdf_template_updated(self, user_id, company_id, form_id, pdf_template_id):
        self.mixpanel.track(user_id, 'PDF Template Updated', {
            'company_id': company_id,
            'form_id': form_id,
            'pdf_template_id': pdf_template_id,
            'company_type': self.define_company_type(user_id)
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
            'kanban_dimension_id': kanban_dimension_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_kanban_default_settings_created(self, user_id, company_id, form_id, kanban_card_id, kanban_dimension_id):
        self.track_kanban_default_settings_updated(user_id, company_id, form_id, kanban_card_id, kanban_dimension_id)
    # ------------------------------------------------------------------------------------------
    def track_kanban_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Kanban Eyeballing', {
            'company_id': company_id,
            'form_id': form_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_listing_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Listing Eyeballing', {
            'company_id': company_id,
            'form_id': form_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_dashboard_loaded(self, user_id, company_id, form_id):
        self.mixpanel.track(user_id, 'Dashboard Eyeballing', {
            'company_id': company_id,
            'form_id': form_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
    def track_notification_loaded(self, user_id, company_id):
        self.mixpanel.track(user_id, 'Notification Eyeballing', {
            'company_id': company_id,
            'company_type': self.define_company_type(user_id)
        })
    # ------------------------------------------------------------------------------------------
