from django.db import models

class UserExtendedFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def timezone_by_user_id(self, user_id):
        return self.get_queryset().filter(id=user_id).values_list('timezone_name', flat=True).first()