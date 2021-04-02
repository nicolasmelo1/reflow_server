from django.db import models


class DefaultFieldValueDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def default_field_values_by_field_ids(self, field_ids):
        return self.get_queryset().filter(field_id__in=field_ids)