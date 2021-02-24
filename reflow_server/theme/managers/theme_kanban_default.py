from reflow_server.theme.managers import theme
from django.db import models


class ThemeKanbanDefaultManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_kanban_defaults_by_theme_id(self, theme_id):
        return self.get_queryset().filter(theme_id=theme_id)

    def create_theme_kanban_default(self, theme_instance, default_kanban_dimension_id, default_kanban_card_id, theme_form_id):
        return self.get_queryset().create(
            theme=theme_instance,
            kanban_dimension_id=default_kanban_dimension_id,
            kanban_card_id=default_kanban_card_id,
            form_id=theme_form_id
        )