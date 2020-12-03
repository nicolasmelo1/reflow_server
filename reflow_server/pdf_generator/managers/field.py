from django.db import models


class FieldPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def fields_by_main_form_id_excluding_form(self, main_form_id):
        return self.get_queryset().filter(form__depends_on_id=main_form_id).exclude(type__type='form')

    def form_fields_by_main_form_id_and_company_id(self, main_form_id, company_id):
        return self.get_queryset().filter(form__depends_on__group__company_id=company_id, form__depends_on_id=main_form_id, type__type='form')