# Generated by Django 3.1.4 on 2021-02-22 16:39

from django.db import migrations, transaction

def get_default_kanban_dimension_id_for_theme_form_id(apps, theme_id, theme_form_id):
    ThemeKanbanDimensionOrder = apps.get_model('theme', 'ThemeKanbanDimensionOrder')
    default_kanban_dimension = ThemeKanbanDimensionOrder.objects.filter(
            theme_id=theme_id,
            default=True,
            dimension__type__type='option',
            dimension__form__depends_on__id=theme_form_id
    ).values_list('dimension_id', flat=True).distinct().first()
    if default_kanban_dimension:
        return default_kanban_dimension
    return None

def get_default_kanban_card_for_theme_form_id(apps, theme_id, theme_form_id):
    ThemeKanbanCard = apps.get_model('theme', 'ThemeKanbanCard')
    ThemeKanbanCardField = apps.get_model('theme', 'ThemeKanbanCardField')
    kanban_card_ids = ThemeKanbanCardField.objects.filter(
        field__form__depends_on__id=theme_form_id, 
        field__form__depends_on__theme_id=theme_id
    ).values_list('kanban_card', flat=True).distinct()
    default_kanban_card_for_form = ThemeKanbanCard.objects.filter(id__in=kanban_card_ids, default=True).first()
    if default_kanban_card_for_form:
        return default_kanban_card_for_form.id
    return None

def add_defaults(apps, theme_id, theme_form_id):
    ThemeKanbanDefault = apps.get_model('theme', 'ThemeKanbanDefault')
    default_theme_kanban_card_id = get_default_kanban_card_for_theme_form_id(apps, theme_id, theme_form_id)
    default_theme_kanban_dimension_id = get_default_kanban_dimension_id_for_theme_form_id(apps, theme_id, theme_form_id)
    if default_theme_kanban_dimension_id and default_theme_kanban_card_id:
        ThemeKanbanDefault.objects.create(
            kanban_card_id=default_theme_kanban_card_id,
            kanban_dimension_id=default_theme_kanban_dimension_id,
            form_id=theme_form_id,
            theme_id=theme_id
        )

def fix_field_option_orders(apps, theme_id, theme_form_id):
    ThemeKanbanDimensionOrder = apps.get_model('theme', 'ThemeKanbanDimensionOrder')
    ThemeFieldOptions = apps.get_model('theme', 'ThemeFieldOptions')
    for theme_dimension_id in ThemeKanbanDimensionOrder.objects.filter(theme_id=theme_id, dimension__form__depends_on__id=theme_form_id).values_list('dimension_id', flat=True).distinct():
        theme_kanban_dimension_options = ThemeKanbanDimensionOrder.objects.filter(
            dimension_id=theme_dimension_id
        ).values_list('options', flat=True).distinct().order_by('order')
        
        theme_field_options = ThemeFieldOptions.objects.filter(field_id=theme_dimension_id)
        field_options_not_in_kanban_dimension = theme_field_options.exclude(option__in=theme_kanban_dimension_options)
        
        order_index = 0
        for theme_kanban_dimension_option in theme_kanban_dimension_options:
            instance = theme_field_options.filter(option=theme_kanban_dimension_option).first()
            if instance:
                instance.order = order_index
                instance.save()

                order_index = order_index + 1

        for field_option_not_in_kanban_dimension in field_options_not_in_kanban_dimension:
            field_option_not_in_kanban_dimension.order = order_index
            field_option_not_in_kanban_dimension.save()

            order_index = order_index + 1

@transaction.atomic
def migrate_add_kanban_defaults_to_theme_kanban_default(apps, schema_editor):
    ThemeForm = apps.get_model('theme', 'ThemeForm')
    
    for theme_form in ThemeForm.objects.filter(depends_on__isnull=True):
        add_defaults(apps, theme_form.theme.id, theme_form.id)
        fix_field_option_orders(apps, theme_form.theme.id, theme_form.id)
    


class Migration(migrations.Migration):

    dependencies = [
        ('theme', '0009_auto_20210222_1639'),
    ]

    operations = [
        migrations.RunPython(migrate_add_kanban_defaults_to_theme_kanban_default)
    ]
