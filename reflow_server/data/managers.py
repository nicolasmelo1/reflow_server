from django.db import models
from django.db.models import Q, Sum, Case, When


class AttachmentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def company_aggregated_file_sizes(self, company_id):
        return self.get_queryset().filter(form__company_id=company_id).aggregate(Sum('file_size')).get('file_size__sum', 0)
    
    def attachment_by_dynamic_form_id_field_id_and_file_name(self,  dynamic_form_id, field_id, file_name):
        return self.get_queryset().filter(Q(form__depends_on_id=dynamic_form_id) | Q(form_id=dynamic_form_id))\
            .filter(field_id=field_id, file=file_name).first()


class FormValueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def form_value_by_company_id_and_form_ids(self, company_id, form_ids):
        return self.get_queryset().filter(company_id=company_id, form_id__in=form_ids)
    
    def form_value_by_company_id_and_form_ids_and_field_ids_ordered(self, company_id, form_ids, field_ids):
        order = Case(*[When(field_id=value, then=pos) for pos, value in enumerate(field_ids)])
        return self.form_value_by_company_id_and_form_ids(company_id, form_ids).filter(field_id__in=field_ids).order_by(order)