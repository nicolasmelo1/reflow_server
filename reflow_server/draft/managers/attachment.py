from django.db import models
from django.db.models import Sum


class AttachmentsDraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def company_aggregated_file_sizes(self, company_id):
        """
        This method calculates the aggregated file size of the attachments for a single company_id

        Args:
            company_id (int): The id of he company you want to aggregate the attachments.

        Returns:
            int: The aggregated file size
        """
        return self.get_queryset().filter(form__company_id=company_id).aggregate(Sum('file_size')).get('file_size__sum', 0)
     