from django.db import models 


class RichTextTextTableOptionRowDimensionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def delete_row_dimensions_by_table_option_id(self, text_table_option_id=None):
        return self.get_queryset().filter(text_table_option_id=text_table_option_id).delete()

    def bulk_create_row_dimensions(self, text_table_option_id, row_dimensions=[]):
        from reflow_server.rich_text.models import TextTableOptionRowDimension

        return self.get_queryset().bulk_create([
            TextTableOptionRowDimension(text_table_option_id=text_table_option_id, order=index, height=height) 
            for index, height in enumerate(row_dimensions)
        ])