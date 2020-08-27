from django.db import models


class DynamicFormKanbanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def sections_data_by_depends_on_id(self, depends_on_id):
        """
        Gets the sections from a depends_on_id.

        Args:
            depends_on_id (int): The DynamicForm instance id that
            the sections depends on

        Returns:
            reflow_server.data.models.DynamicForm: The DynamicForm instances
            of a formualry data id.
        """
        return self.get_queryset().filter(depends_on_id=depends_on_id)