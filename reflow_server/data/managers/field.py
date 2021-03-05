from django.db import models


class FieldDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def fields_enabled_ordered_by_form_and_order_by_main_form_name_and_sections(self, main_form_name, sections):
        return self.get_queryset().filter(
            form__depends_on__form_name= main_form_name,
            form__id__in=sections,
            form__enabled=True,
            enabled=True
        ).order_by('form__order', 'order')