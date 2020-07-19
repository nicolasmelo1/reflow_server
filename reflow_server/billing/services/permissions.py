from django.conf import settings
from django.db.models import Sum
from django.utils import timezone

from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.authentication.models import Company
from reflow_server.data.models import Attachments

import functools


class BillingPermissionService:
    def __init__(self, company_id, url_name=None, files=None):
        self.company = Company.objects.filter(id=company_id).first()

        if url_name:
            self.url_name = url_name
        
        if files:
            self.files = files

    def is_valid_file(self):
        """validates the billing"""
        from reflow_server.core.utils.routes import attachment_url_names

        if self.url_name in attachment_url_names:
            company_aggregated_file_sizes = Attachments.objects.filter(form__company=self.company).aggregate(Sum('file_size')).get('file_size__sum', 0)
            current_gb_permission_for_company = CurrentCompanyCharge.objects.filter(individual_charge_value_type__name='per_gb', company=self.company).values_list('quantity', flat=True).first()

            new_files_size = functools.reduce(
                lambda x, y: x + y, [
                    file_data.size for key in self.files.keys() for file_data in self.files.getlist(key)
                ], 0
            ) * 0.000000001
            company_aggregated_file_sizes = company_aggregated_file_sizes if company_aggregated_file_sizes else 0
            company_aggregated_file_sizes = company_aggregated_file_sizes * 0.000000001
            all_file_sizes = new_files_size + company_aggregated_file_sizes
            # if the size of the files saved in the database + the size of this new file is less than the current_gb_permitted 
            # for the company
            if all_file_sizes < current_gb_permission_for_company:
                return True
            else:
                return False
        else:
            return True
    
    def is_valid_free_trial(self):
        if not self.company.is_paying_company and self.company.created_at < timezone.now() - timedelta(days=settings.FREE_TRIAL_DAYS):
            return False
        else:
            return True

    def is_valid(self):
        # we only validate the billing if the company is not a supercompany, if the company IS a supercompany we pass all 
        # of the billing validation.
        if not self.company.is_supercompany:
            if hasattr(self, 'url_name') and hasattr(self, 'files'):
                if not self.is_valid_file():
                    return False
            
        return True