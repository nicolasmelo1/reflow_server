from django.db import models 


class RichTextTextTableOptionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def update_or_create(self, border_color, text_table_option_id=None):
        instance, __ = self.get_queryset().update_or_create(
            id=text_table_option_id,
            defaults={
                'border_color': border_color
            }
        )

        return instance