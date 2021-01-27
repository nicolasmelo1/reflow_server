from django.db import models 


class TextTableOptionColumnDimensionRichTextManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def delete_column_dimensions_by_table_option_id(self, text_table_option_id=None):
        return self.get_queryset().filter(text_table_option_id=text_table_option_id).delete()

    def bulk_create_column_dimensions(self, text_table_option_id, column_dimensions=[]):
        from reflow_server.rich_text.models import TextTableOptionColumnDimension

        return self.get_queryset().bulk_create([
            TextTableOptionColumnDimension(text_table_option_id=text_table_option_id, order=index, width=width) 
            for index, width in enumerate(column_dimensions)
        ])