from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.models import Form


class SectionService(Settings):
    def __init__(self, user_id, form_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form_id = form_id

    def save_section(self, enabled, label_name, order, conditional_value, 
                     section_type, conditional_type, conditional_on_field, instance=None):
            existing_sections = Form.objects.filter(
                depends_on__group__company_id=self.company_id, 
                depends_on_id=self.form_id
            ).order_by('order')
            self.update_order(existing_sections, order)
            
            if instance == None:
                instance = Form()

            instance.depends_on_id = self.form_id
            instance.company_id = self.company_id
            instance.enabled=enabled
            instance.label_name=label_name
            instance.order=order
            instance.conditional_value=conditional_value
            instance.type=section_type
            instance.conditional_type=conditional_type
            instance.conditional_on_field=conditional_on_field
            instance.form_name = self.format_name('form', instance.id, instance.form_name, label_name)
            instance.save()
            return instance