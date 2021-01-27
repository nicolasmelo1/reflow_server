from django.db import models 


class TextTableOptionRichTextManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def update_or_create(self, border_color, text_table_option_id=None):
        """
        Updates or crates a new TextTableOption instance in the database. This model holds only the border_color
        but it also is used as reference for the number of columns and rows for TextTableOptionColumnDimension and 
        TextTableOptionRowDimension respectively.

        Args:
            border_color (str): The hex string of the border color
            text_table_option_id (int, optional): If you are editing a TextTableOption instance, this is the id of the 
            instance that's being edited. Defaults to None.

        Returns:
            reflow_server.rich_text.models.TextTableOption: The created or updated TextTableOption instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            id=text_table_option_id,
            defaults={
                'border_color': border_color
            }
        )

        return instance