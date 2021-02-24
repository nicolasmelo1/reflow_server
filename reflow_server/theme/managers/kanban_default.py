from django.db import models


class KanbanDimensionThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def kanban_default_by_user_id_company_id_and_main_form_ids(self, user_id, company_id, form_ids):
        return self.get_queryset().filter(user_id=user_id, company_id=company_id, form_id__in=form_ids)