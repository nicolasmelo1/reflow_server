from django.db import models


class OptionAccessedByKanbanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def field_options_by_user_id_and_field_id(self, user_id, field_id):
        return self.get_queryset().filter(user_id=user_id, field_option__field_id=field_id).values_list('field_option', flat=True)