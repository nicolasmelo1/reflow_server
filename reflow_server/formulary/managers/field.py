from django.db import models
from django.db.models import Q

class FieldFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def field_by_label_name_company_id_and_main_form_id_excluding_id_exists(self, field_id, label_name, company_id, main_form_id):
        return self.get_queryset().filter(label_name=label_name, form__depends_on_id=main_form_id, form__company_id=company_id).exclude(id=field_id).exists()

    def field_by_field_id_main_form_id_and_company_id(self, field_id, company_id):
        return self.get_queryset().filter(
            id=field_id,
            form__depends_on__group__company_id=company_id
        ).first()

    def fields_by_company_id_excluding_main_form_id_attachments_and_multi_forms(self, company_id, main_form_id):
        return self.get_queryset().filter(
                form__depends_on__group__company_id=company_id
            ).exclude(
                form__depends_on_id=main_form_id
            ).exclude(
                Q(type__type='attachment') | 
                Q(form__type__type__in=['multi-form'])
            )