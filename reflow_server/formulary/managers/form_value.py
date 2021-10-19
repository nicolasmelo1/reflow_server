from django.db import models


class FormValueFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def distinct_main_form_id_by_company_id_field_id_search_value_and_form_id(self, company_id, field_id, search=None, section_id=None):
        """
        Gets a queryset of FormValue instances based on a company_id and a field_id.

        Args:
            company_id (int): This is the company_id to retrieve FormValue instances from
            field_id (int): The field_id to retrieve FormValue instances from
            search (str): This is the value you want to search in our app. Defaults to None.
            section_id (str): This is the section id of this field. We will use this to get the value directly. 
                              Defaults to None.
                              
        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValue instances 
                                                                            based on the parameters
        """
        if search:
            return self.get_queryset().filter(
                company_id=company_id, 
                field_id=field_id, 
                value__icontains=search
            ).values_list('form__depends_on_id', flat=True).distinct()
        elif section_id and str(section_id).isdigit(): 
            return self.get_queryset().filter(
                company_id=company_id, 
                field_id=field_id, 
                form_id=int(section_id)
            ).values_list('form__depends_on_id', flat=True).distinct()
        else:
            return self.get_queryset().filter(
                company_id=company_id, 
                field_id=field_id
            ).values_list('form__depends_on_id', flat=True).distinct()

    def latest_form_value_field_type_by_field_id(self, field_id):
        return self.get_queryset().filter(field_id=field_id).order_by('-updated_at').first()