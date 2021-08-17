from django.conf import settings
from django.utils import timezone

from reflow_server.authentication.models import Company
from reflow_server.billing.models import CompanyBilling

from datetime import timedelta


class BillingPermissionsService:
    @staticmethod
    def is_valid_free_trial(company_id):
        company = Company.billing_.company_by_company_id(company_id)
        company_billing = CompanyBilling.objects.filter(company_id=company_id).first()
        if company and company_billing:
            if not company_billing.is_paying_company and \
                company.created_at < timezone.now() - timedelta(days=settings.FREE_TRIAL_DAYS):
                return False
            else:
                return True
        else:
            return False
