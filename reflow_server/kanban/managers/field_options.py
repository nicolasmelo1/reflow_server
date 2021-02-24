from django.db import models


class FieldOptionsKanbanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def field_options_by_field_option_ids_and_company_id(self, field_option_ids, company_id):
        return self.get_queryset().filter(
            id__in=field_option_ids,
            field__form__depends_on__group__company_id=company_id    
        )