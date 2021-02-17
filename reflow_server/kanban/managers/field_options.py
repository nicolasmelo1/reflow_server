from django.db import models


class FieldOptionsKanbanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def field_options_by_dimension_id_main_form_name_and_company_id(self, dimension_id, form_name, company_id):
        return self.get_queryset().filter(
            field_id=dimension_id, 
            field__form__depends_on__form_name=form_name,
            field__form__depends_on__group__company_id=company_id    
        )