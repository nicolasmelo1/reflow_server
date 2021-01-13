from reflow_server.formulary.models import FormAccessedBy, Form, SectionType
from reflow_server.formulary.services.utils import Settings


class FormularyService(Settings):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id

    def is_user_able_to_access_the_formulary(self, form_id):
        return FormAccessedBy.objects.filter(form_id=self.section.depends_on_id, user=self.user).exists()
    
    def formularies_the_user_has_access_to(self):
        return [
            {
                'form_name': form_a_user_has_access_to.form__name, 
                'form_id': form_a_user_has_access_to.form_id
            } for form_a_user_has_access_to in FormAccessedBy.objects.filter(user_id=self.user_id).values('form_id', 'form__form_name')
        ]
    
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

    @property
    def formulary_ids_the_user_has_access_to(self):
        return FormAccessedBy.objects.filter(user_id=self.user_id, form__enabled=True)\
            .order_by('form__order')\
            .values_list('form_id', flat=True)

    @property
    def formulary_names_the_user_has_access_to(self):
        return FormAccessedBy.objects.filter(user_id=self.user_id, form__enabled=True, form__depends_on__isnull=True)\
            .order_by('form__order')\
            .values_list('form__form_name', flat=True)

    def save_formulary(self, enabled, label_name, order, group, instance=None):
        if instance == None:
            instance = Form()
            
        existing_forms = Form.objects.filter(group__company_id=self.company_id, depends_on__isnull=True)\
                                     .exclude(id=instance.id if instance else None)\
                                     .order_by('group__order', 'order')
        self.update_order(existing_forms, order)

        is_new = instance.id == None

        instance.company_id = self.company_id
        instance.enabled = enabled
        instance.label_name = label_name
        instance.order = order
        instance.group = group
        instance.type = SectionType.objects.filter(type='form').first()
        instance.form_name = self.format_name('form', instance.id, instance.form_name, label_name)
        instance.save()

        if is_new:
            FormAccessedBy.objects.create(form=instance, user_id=self.user_id)
        return instance
    