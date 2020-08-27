from django.db import models


class FormValueFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
        
    def form_values_by_company_id_and_field_id(self, company_id, field_id):
        """
        Gets a queryset of FormValue instances based on a company_id and a field_id.

        Args:
            company_id (int): This is the company_id to retrieve FormValue instances from
            field_id (int): The field_id to retrieve FormValue instances from

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValue instances 
                                                                            based on the parameters
        """
        return self.get_queryset().filter(company_id=company_id, field_id=field_id)
