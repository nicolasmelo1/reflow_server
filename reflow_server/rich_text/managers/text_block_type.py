from django.db import models


class RichTextTextBlockTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all_block_types(self):
        """
        Gets all the block types.

        Returns:
            django.db.models.QuerySet(reflow_server.rich_text.models.TextBlockType): returns the Queryset of all of the TextBlockTypes.
        """
        return self.get_queryset().all()
