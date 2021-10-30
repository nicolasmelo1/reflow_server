from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.authentication.models import Company, UserExtended, ProfileType, VisualizationType
from reflow_server.authentication.services.company import CompanyService
from reflow_server.authentication.services.users import UsersService
from reflow_server.billing.services import BillingService
from reflow_server.formula.services.formula import FlowFormulaService
from reflow_server.analytics.models import CompanyAnalytics


class OnboardingService(CompanyService):
    """
    Service used to onboard a user to Reflow, used on onboarding

    Available Methods:
    .onboard()
    """
    @transaction.atomic
    def onboard(self, user_email, user_first_name, user_last_name, user_password, 
                user_phone, company_name=None, company_number_of_employees=0, company_sector='',
                shared_by=None, partner=None, discount_coupon_name=None, user_visitor_id=''):
        """
        Onboards a new user and creates a new company (aswell as a new user). Updates the billing info on the fly.

        Arguments:
            user_email (str): The user email
            user_first_name (str): The first name of the user
            user_last_name (str): the last name of the user you want to onboard
            user_password (str): The new password of the user
            user_phone (str): The phone number of the user

        Keyword Arguments:
            company_name (str): the company name, if it has one (default: {None})
            company_number_of_employees (str): The number of employees of the company.
            company_sector (str): The market sector that the company operates.
            shared_by (str): the string of the company endpoint if it was shared by some other company (default: {None})
            partner (str): The string of the partner if the user came from a partner. (default: {None})
            discount_coupon (str): The string of the discount coupon to use.
            user_visitor_id (str): The user visitor id, this is the id we set with reflow_tracking application for the user (default: '')
        
        Returns:
            reflow_server.authentication.models.UserExtended -- returns the created user.
        """
        if company_name in [None, '']: 
            company_name = self._company_name_generator()

        if shared_by:
            shared_by = Company.authentication_.company_by_endpoint(shared_by)

        company = Company.authentication_.create_company(
            company_name=company_name,
            company_endpoint=self._create_company_endpoint(company_name),
            shared_by=shared_by,
            partner=partner
        )

        CompanyAnalytics.authentication_.create_company_analytics(
            company.id,
            company_number_of_employees,
            company_sector
        )
        
        admin_profile_id = ProfileType.objects.get(name='admin').id

        visualization_type_id = VisualizationType.objects.filter(name='listing').values_list('id', flat=True).first()

        user = UserExtended.authentication_.create_user(
            user_email,
            user_first_name,
            user_last_name,
            company.id,
            admin_profile_id,
            visualization_type_id,
            user_phone,
            user_password
        )

        # Sends events that the user is onboarding on our platform
        Event.register_event('user_onboarding', {
            'user_id': user.id,
            'company_id': company.id,
            'visitor_id': user_visitor_id
        })
        
        # Added api acess for newly created user since he cannot edit itself
        # TODO: need to change this once the user can edit himself
        UsersService.update_api_access_key_of_user(company.id, user.id, True)
        # update billing information
        BillingService.create_on_onboarding(company.id, user.id, partner, discount_coupon_name)
        # updates formula context
        FlowFormulaService.update_company_formula_context(company)
        return user
