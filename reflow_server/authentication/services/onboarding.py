from reflow_server.authentication.models import Company, UserExtended, ProfileType
from reflow_server.authentication.services.company import CompanyService

class OnboardingService(CompanyService):
    """
    Service used to onboard a user to Reflow, used on onboarding

    Available Methods:
    .onboard()
    """
    def onboard(self, user_email, user_first_name, user_last_name, user_password, company_name=None, shared_by=None, partner=None):
        """
        Onboards a new user and creates a new company (aswell as a new user). Updates the billing info on the fly.

        Arguments:
            user_email {str} -- The user email
            user_first_name {str} -- The first name of the user
            user_last_name {str} -- the last name of the user you want to onboard
            user_password {str} -- The new password of the user

        Keyword Arguments:
            company_name {str} -- the company name, if it has one (default: {None})
            shared_by {str} -- the string of the company endpoint if it was shared by some other company (default: {None})
            partner {str} -- The string of the partner if the user came from a partner. (default: {None})

        Returns:
            reflow_server.authentication.models.UserExtended -- returns the created user.
        """
        if company_name: 
            company_name = self._company_name_generator()

        if shared_by:
            shared_by = Company.objects.filter(endpoint=shared_by).first()

        company = Company.objects.create(
            name=company_name,
            endpoint=self._create_company_endpoint(company_name),
            shared_by=shared_by,
            partner=partner
        )

        user = UserExtended.objects.create(
            username=user_email,
            email=user_email,
            first_name=user_first_name,
            last_name=user_last_name,
            company=company,
            profile=ProfileType.objects.get(name='admin')
        )
        user.set_password(user_password)
        user.save()
        
        # update billing information
        company_billing = BillingService(company.id)
        company_billing.update_company()

        return user