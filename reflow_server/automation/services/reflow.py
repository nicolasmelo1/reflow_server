from reflow_server.automation.services import AutomationService

from reflow_server.formulary.models import Form, Field


formulary_cache = {}

class ReflowAutomationService:
    def __init__(self, company_id, user_id):
        """
        Service responsible for running reflow automations so instead of calling webhooks directly
        we will just initialize this method and call the functions directly to activate the trigger
        and actions.

        Args:
            company_id (int): Company instance id
            user_id (int): UserExtended instance id
        """
        self.user_id = user_id
        self.company_id = company_id
    
    def build_formulary_data_on_hooks(self, formulary_id, data):
        """
        This builds the formulary data on a more user friendly way, the data is build on some foundations for programmers
        so we need to format in some way that users can work easily, also we want need to build this in some way that we 
        can use in flow Reflow.create_record() function.

        Args:
            formulary_id (int): A DynamicForm instance id where depends_on is None.
            data (reflow_server.data.services.data.FormularyData): A formulary data instance object with all of the data from
            the formulary.
        """
        if formulary_cache.get(formulary_id, None) and formulary_cache[formulary_id]['usage_count'] < 100:
            formulary_label_name = formulary_cache[formulary_id]['formulary_label_name']
            group_name = formulary_cache[formulary_id]['group_name']
            section_reference = formulary_cache[formulary_id]['section_reference']
            field_reference = formulary_cache[formulary_id]['field_reference']
            
            formulary_cache[formulary_id]['usage_count'] += 1
        else:
            formulary_instance = Form.objects.filter(id=formulary_id).values('label_name', 'group__name').first()
            formulary_label_name = formulary_instance['label_name']
            group_name = formulary_instance['group__name']
            section_instances = Form.objects.filter(depends_on_id=formulary_id).values('id', 'label_name')
            field_instances = Field.objects.filter(form__depends_on_id=formulary_id).values('id', 'label_name')
            section_reference = { section_instance['id']:section_instance['label_name'] for section_instance in section_instances }
            field_reference = { field_instance['id']:field_instance['label_name'] for field_instance in field_instances }

            formulary_cache[formulary_id] = {
                'usage_count': 1,
                'formulary_label_name':formulary_label_name,
                'group_name': group_name,
                'section_reference': section_reference,
                'field_reference': field_reference
            }

        new_data = {
            'formulary_label_name': formulary_label_name,
            'group_name': group_name,
            'record_data': {}
        }

        sections = data.get_sections
        for section in sections:
            # TODO: If multisection, transform to list
            if section_reference.get(section.section_id, None):
                section_label_name = section_reference[section.section_id]
                section_data = {}
                
                field_values = section.get_field_values
                # TODO: if multi value, transform to list
                for field_value in field_values:
                    if field_reference.get(field_value.field_id, None):
                        field_label_name = field_reference[field_value.field_id]
                        if field_label_name not in section_data:
                            section_data[field_label_name] = field_value.value
                        elif not isinstance(section_data[field_label_name], list):
                            # transform to a list and append the new value
                            section_data[field_label_name] = [section_data[field_label_name], field_value.value]
                        elif isinstance(section_data[field_label_name], list):
                            section_data[field_label_name].append(field_value.value)

                if section_label_name not in new_data['record_data']:
                    new_data['record_data'][section_label_name] = section_data
                # it is a multisection so transform it in a list
                elif isinstance(new_data['record_data'][section_label_name], dict):
                    new_data['record_data'][section_label_name] = [new_data['record_data'][section_label_name], section_data]
                elif isinstance(new_data['record_data'][section_label_name], list):
                    new_data['record_data'][section_label_name].append(section_data)
        return new_data
    
    def formulary_data_created(self, formulary_id, main_formulary_id, data):
        data = self.build_formulary_data_on_hooks(formulary_id, data)
        automation_service = AutomationService(self.company_id)
        automation_service.trigger(self.user_id, 'reflow', 'formulary_data_created', {
            'record_id': main_formulary_id,
            'formulary_name': data['formulary_label_name'],
            'group_name': data['group_name'],
            'data': data['record_data']
        })

    def formulary_data_updated(self, formulary_id, main_formulary_id, data):
        data = self.build_formulary_data_on_hooks(formulary_id, data)
        trigger_data = {
            'record_id': main_formulary_id,
            'formulary_name': data['formulary_label_name'],
            'group_name': data['group_name'],
            'data': data['record_data']
        }
        automation_service = AutomationService(self.company_id)
        automation_service.trigger(self.user_id, 'reflow', 'formulary_data_updated', trigger_data)