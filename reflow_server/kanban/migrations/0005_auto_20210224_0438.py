# Generated by Django 3.1.4 on 2021-02-24 04:38

from django.db import migrations

def migrate_add_order_to_kanban_card_field(apps, schema_editor):
    KanbanCardField = apps.get_model('kanban', 'KanbanCardField')

    last_kanban_card_id = None
    order = 0
    for kanban_card_field in KanbanCardField.objects.all().order_by('kanban_card_id', 'id'):
        if kanban_card_field.kanban_card.id != last_kanban_card_id:
            order = 0
        else:
            order = order + 1
        kanban_card_field.order = order
        kanban_card_field.save()

        last_kanban_card_id = kanban_card_field.kanban_card.id
        

class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0004_kanbancardfield_order'),
    ]

    operations = [
        migrations.RunPython(migrate_add_order_to_kanban_card_field)
    ]
