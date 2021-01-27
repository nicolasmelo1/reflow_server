from django.db import models


class TextBlockTypeCanContainTypeRichTextManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all_block_type_can_contain_types(self):
        """
        Returns all of the block types another block can contain. So when a block has children blocks
        we can filter what those children blocks should be.

        Returns:
            django.db.models.QuerySet(reflow_server.rich_text.models.TextBlockTypeCanContainType): A queryset
            of all of the textBlockIds and what block_id each of them can contain.
        """
        return self.get_queryset().all()