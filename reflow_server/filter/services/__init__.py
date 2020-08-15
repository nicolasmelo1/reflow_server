from django.db.models import Q
from reflow_server.filter.models import Filter, FilterCondition, FilterConditionalType, FilterConectorType



class FilterConditionData:
    def __init__(self, field_id, conditional, value, connector=None): 
        self.conditional = conditional
        self.field_id = field_id
        self.value = value
        self.connector = connector
        

class FilterDataService:
    def __init__(self, form_data_ids_to_filter, filter_id):
        conditions = FilterCondition.objects.filter(id=filter_id)
        self.conditions_data = []

        for condition in conditions:
            conditional_name = FilterConditionalType.objects.filter(id=condition.conditional_type).first()
            connector_name = FilterConectorType.objects.filter(id=condition.conector_type).first()
            if (condition.conditional_type and not conditional_name) or (condition.conector_type and not connector_name):
                raise AssertionError(
                    'Looks like the conditional or the connector you are trying to use for this does not exist'
                )
            self.conditions_data.append(FilterConditionData(condition.field.id, conditional_name, condition.value, connector_name))

    def get_django_q_objects(self):
        # Reference https://stackoverflow.com/a/50775442
        filter_conditionals = Q()
        exclude_conditionals = Q()

        for condition in self.conditions:
            if 'contains' in condition.conditional:
                conditional = {'field_id': condition.field_id, 'value__icontains': value }
            else:
                conditional = {'field_id': condition.field_id, 'value': value }

            if 'not' in condition.conditional:
                exclude_conditionals.add(Q(**conditional), Q.OR if condition.connector == 'or' else Q.AND)
            else: 
                filter_conditionals.add(Q(**conditional), Q.OR if condition.connector == 'or' else Q.AND)
        
        return [filter_conditionals, exclude_conditionals]

    def search(self):
        [filter_conditionals, exclude_conditionals] = self.get_django_q_objects()
