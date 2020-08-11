from django.conf import settings
from django.db.models import Sum
from django.utils import timezone

from reflow_server.authentication.models import Company
from reflow_server.data.models import Attachments

from datetime import timedelta
import functools


class BillingPermissionsService:
    @staticmethod
    def is_valid_free_trial(company_id):
        company = Company.objects.filter(id=company_id).first()
        if company:
            if not company.is_paying_company and \
                company.created_at < timezone.now() - timedelta(days=settings.FREE_TRIAL_DAYS):
                return False
            else:
                return True
        else:
            return False
