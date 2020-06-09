from reflow_server.formulary.models import FormAccessedBy, Form, FormType
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
            } for form_a_user_has_access_to in FormAccessedBy.objects.filter(user=self.user).values('form_id', 'form__form_name')
        ]
    
    def formulary_ids_the_user_has_access_to(self):
        return FormAccessedBy.objects.filter(user=self.user).values('form_id', flat=True)

    def formulary_names_the_user_has_access_to(self):
        return FormAccessedBy.objects.filter(user=self.user).values('form__form_name', flat=True)

    def save_formulary(self, instance, enabled, form_name, label_name, order, group):
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
        instance.type = FormType.objects.filter(type='form').first()
        instance.form_name = self.format_name('form', instance.id, '', label_name)
        instance.save()

        if is_new:
            FormAccessedBy.objects.create(form=instance, user_id=self.user_id)
        return instance
    