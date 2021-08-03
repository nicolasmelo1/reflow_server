from reflow_server.formulary.models import FormAccessedBy, Form, SectionType
from reflow_server.formulary.services.utils import Settings
from reflow_server.core.events import Event

import uuid


class FormularyService(Settings):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
    # ------------------------------------------------------------------------------------------
    def update_formulary_ids_the_user_has_access_to(self, form_ids):
        """
        Adds a list of form_ids to the `FormAccessedBy` model and deletes the ones that he does not have
        access anymore

        Args:
            form_ids (list(int)): A list of form_ids, this list are the form_ids the user has access to. The ones that are not in this list
                                  are removed from the user.

        Returns:
            bool: returns True to show everything went fine.
        """
        # exclude all of the form_ids not in list
        FormAccessedBy.objects.filter(user_id=self.user_id).exclude(form_id__in=form_ids).delete()
        already_existing_form_ids_the_user_can_access = FormAccessedBy.objects.filter(
            user_id=self.user_id, 
            form_id__in=form_ids
        ).values_list('form_id', flat=True)
        for form_id in form_ids:
            if form_id not in already_existing_form_ids_the_user_can_access:
                FormAccessedBy.objects.create(user_id=self.user_id, form_id=form_id)

        return True
    # ------------------------------------------------------------------------------------------
    @property
    def formulary_ids_the_user_has_access_to(self):
        return FormAccessedBy.formulary_.main_form_ids_accessed_by_user_id_and_enabled_ordered_by_order(self.user_id)
    # ------------------------------------------------------------------------------------------
    @property
    def formulary_names_the_user_has_access_to(self):
        return FormAccessedBy.formulary_.main_form_names_accessed_by_user_id_and_enabled_ordered_by_order(self.user_id)
    # ------------------------------------------------------------------------------------------
    def save_formulary(self, enabled, label_name, order, group, formulary_uuid=None, instance=None, is_adding_theme=False):
        """
        Saves a new formulary or updates an existing formulary. When the formulary is added `instance` will be None,
        otherwise `instance` will be the instance to replace the data to.
        """
        if instance == None:
            instance = Form()
            
        if formulary_uuid == None:
            formulary_uuid = uuid.uuid4()

        existing_forms = Form.objects.filter(group__company_id=self.company_id, depends_on__isnull=True)\
                                     .exclude(id=instance.id if instance else None)\
                                     .order_by('group__order', 'order')
                                     
        self.update_order(existing_forms, order, instance.id if instance else None)

        is_new = instance.id == None

        instance.company_id = self.company_id
        instance.enabled = enabled
        instance.uuid = formulary_uuid
        instance.label_name = label_name
        instance.order = order
        instance.group = group
        instance.type = SectionType.objects.filter(type='form').first()
        instance.form_name = self.format_name('form', instance.id, instance.form_name, label_name)
        instance.save()

        events_data = {
            'user_id': self.user_id,
            'company_id': self.company_id,
            'form_id': instance.id
        }
        if is_adding_theme == False:
            if is_new:
                FormAccessedBy.objects.create(form=instance, user_id=self.user_id)
                Event.register_event('formulary_created', events_data)
            else:
                Event.register_event('formulary_updated', events_data)
        return instance
    