# Generated by Django 3.1.4 on 2021-02-20 05:56
from django.db import migrations, transaction


def get_default_kanban_dimension_id(apps, user_id, company_id, form_id):
    KanbanDimensionOrder = apps.get_model('kanban', 'KanbanDimensionOrder')
    default_kanban_dimension = KanbanDimensionOrder.objects.filter(
            user_id=user_id,
            default=True,
            dimension__type__type='option',
            dimension__form__depends_on__id=form_id
    ).values_list('dimension_id', flat=True).distinct().first()
    if default_kanban_dimension:
        return default_kanban_dimension
    return None

def get_default_kanban_card_of_user_by_form_id(apps, user_id, company_id, form_id):
    KanbanCard = apps.get_model('kanban', 'KanbanCard')
    KanbanCardField = apps.get_model('kanban', 'KanbanCardField')
    kanban_card_ids = KanbanCardField.objects.filter(
        field__form__depends_on__id=form_id, 
        field__form__depends_on__group__company_id=company_id,
        kanban_card__user_id=user_id
    ).values_list('kanban_card', flat=True).distinct()
    default_kanban_card_for_form = KanbanCard.objects.filter(id__in=kanban_card_ids, default=True).first()
    if default_kanban_card_for_form:
        return default_kanban_card_for_form.id
    return None

def reorder_field_options(apps, admin_user_to_use_as_reference):
    FieldOptions = apps.get_model('formulary', 'FieldOptions')
    KanbanDimensionOrder = apps.get_model('kanban', 'KanbanDimensionOrder')

    # loop through each dimension_id of the user and use this
    for dimension_id in KanbanDimensionOrder.objects.filter(user_id=admin_user_to_use_as_reference.id).values_list('dimension_id', flat=True).distinct():
        kanban_dimension_options = KanbanDimensionOrder.objects.filter(
            dimension_id=dimension_id
        ).values_list('options', flat=True).distinct().order_by('order')
        
        field_options = FieldOptions.objects.filter(field_id=dimension_id)
        field_options_not_in_kanban_dimension = field_options.exclude(option__in=kanban_dimension_options)
        
        order_index = 0
        for kanban_dimension_option in kanban_dimension_options:
            instance = field_options.filter(option=kanban_dimension_option).first()
            if instance:
                instance.order = order_index
                instance.save()

                order_index = order_index + 1

        for field_option_not_in_kanban_dimension in field_options_not_in_kanban_dimension:
            field_option_not_in_kanban_dimension.order = order_index
            field_option_not_in_kanban_dimension.save()

            order_index = order_index + 1
        

def add_defaults_and_reorder_field_options(apps):
    Company = apps.get_model('authentication', 'Company')
    UserExtended = apps.get_model('authentication', 'UserExtended')
    FormAccessedBy = apps.get_model('formulary', 'FormAccessedBy')
    KanbanDefault = apps.get_model('kanban', 'KanbanDefault')

    # loop on all companies
    for company in Company.objects.all():
        # get user to use as reference for the defaults, this user is the first admin created of a specific company
        admin_user_to_use_as_reference = UserExtended.objects.filter(profile__name='admin', company=company, is_active=True).earliest('date_joined')

        for user in UserExtended.objects.filter(company=company):
            for form_accessed_by in FormAccessedBy.objects.filter(user=user):
                default_kanban_card_id = get_default_kanban_card_of_user_by_form_id(apps, user.id, company.id, form_accessed_by.form.id)
                default_kanban_dimension_id = get_default_kanban_dimension_id(apps, user.id, company.id, form_accessed_by.form.id)

                if default_kanban_card_id and default_kanban_dimension_id:
                    KanbanDefault.objects.create(
                        form=form_accessed_by.form,
                        company=company,
                        user=user,
                        kanban_card_id=default_kanban_card_id,
                        kanban_dimension_id=default_kanban_dimension_id
                    )
                
        reorder_field_options(apps, admin_user_to_use_as_reference)
            
@transaction.atomic
def migrate_kanban_to_new_tables_and_add_columns_to_kanban_card(apps, schema_editor):
    add_defaults_and_reorder_field_options(apps)

class Migration(migrations.Migration):

    dependencies = [
        ('kanban', '0002_auto_20210220_0556'),
    ]

    operations = [
        migrations.RunPython(migrate_kanban_to_new_tables_and_add_columns_to_kanban_card)
    ]
