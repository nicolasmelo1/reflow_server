from reflow_server.billing.services import BillingService
from reflow_server.data.models import Attachments
from reflow_server.rich_text.models import TextImageOption
from reflow_server.billing.models import CurrentCompanyCharge

import functools


class DraftPermissionService:
    @staticmethod
    def validate_file_upload(company_id, files):
        """
        We set a limit to the quantity of GBs each company can store files.
        Because of this we need to validate when the users of this company attach a new file on the draft.

        The way it works is: We have a IndividualChargeType called 'per_gb'. So what we do when the user is saving a 
        new draft is simple: we check the size of the files he appended on the request and get the size of all files he have in our database.

        If the sum of: size_of_all_files_appended_on_this_request + size_of_all_files_appended_historically is bigger than the quantity this
        company has the request fails. Otherwise everything runs fine.

        Args:
            company_id (int): 'per_gb' are always bound to the hole company
            files (django.http.HttpRequest.FILES): The files appended on the request so we can validate the size of them.

        Returns:
            bool: true if is valid, so everything can go as normal, and false if not valid, so needs to notify the user he can't do this operation.
        """
        company_aggregated_rich_text_image_sizes = TextImageOption.draft_.company_aggregated_image_sizes(company_id)
        company_aggregated_attachment_file_sizes = Attachments.draft_.company_aggregated_file_sizes(company_id)
        
        company_aggregated_rich_text_image_sizes = company_aggregated_rich_text_image_sizes if company_aggregated_rich_text_image_sizes else 0
        company_aggregated_attachment_file_sizes = company_aggregated_attachment_file_sizes if company_aggregated_attachment_file_sizes else 0

        current_gb_permission_for_company = CurrentCompanyCharge.objects.filter(
            individual_charge_value_type__name='per_gb', 
            company_id=company_id
        ).values_list('quantity', flat=True).first()

        new_files_size = functools.reduce(
            lambda x, y: x + y, [
                file_data.size for key in files.keys() for file_data in files.getlist(key)
            ], 0
        ) * 0.000000001
        company_aggregated_file_sizes = company_aggregated_attachment_file_sizes + company_aggregated_rich_text_image_sizes
        company_aggregated_file_sizes = company_aggregated_file_sizes if company_aggregated_file_sizes else 0
        company_aggregated_file_sizes = company_aggregated_file_sizes * 0.000000001
        all_file_sizes = new_files_size + company_aggregated_file_sizes
        # if the size of the files saved in the database + the size of this new file is less than the current_gb_permitted 
        # for the company
        if all_file_sizes < current_gb_permission_for_company:
            return False
        return True

