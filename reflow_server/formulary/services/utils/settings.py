from reflow_server.core.utils import replace_dumb_characters_from_str
from reflow_server.formulary.utils.order import Order
from reflow_server.formulary.models import Field, Form

import unicodedata
import string
import random
import re


class Settings:
    def __init__(self, company_id):
        self.company_id = company_id
        self.insert = 1
    
    def format_name(self, form_or_field, instance_id, old_name, label_name):
        if form_or_field not in ['form', 'field']:
            raise KeyError('`form_or_field` parameter must be a string with one of the following options: `form`, `field`')

        new_name = replace_dumb_characters_from_str(
                        unicodedata.normalize('NFKD', label_name.lower().replace(' ', '_'))
                            .encode('ascii', 'ignore').decode('utf-8').translate(
                        str.maketrans('', '', string.punctuation))
                    )
        if old_name and new_name in old_name:
            return old_name
        else:
            return self.__check_if_name_exists(form_or_field, instance_id, new_name)

    def __check_if_name_exists(self, form_or_field, instance_id, name):
        name = replace_dumb_characters_from_str(
            unicodedata.normalize('NFKD', name.lower().replace(' ', '_')).encode('ascii', 'ignore').decode('utf-8').translate(str.maketrans('', '', string.punctuation)))
        pattern = re.compile('\d+', re.IGNORECASE)
        # adds an _ if the name is only number, we use this because of the id, there`s a small chance a fieldname have the same name as the id,
        # which can cause some problems, to supress it we add an unerline if the field contains just numbers.
        if pattern.match(name):
            name = name + '_'
        if not instance_id:
            instance_id = None
        
        new_name = name
        while self._has_form_or_field_with_name(form_or_field, new_name, instance_id):
            number = random.randint(1,1000)
            new_name = name + '_' + str(number)
        return new_name

    def _has_form_or_field_with_name(self, form_or_field, name, instance_id):
        if form_or_field == 'form':
            does_with_name_exists = Form.objects.filter(group__company_id=self.company_id, form_name=name).exclude(pk=instance_id).exists()
        else:
            does_with_name_exists = Field.objects.filter(form__depends_on__group__company_id=self.company_id, name=name).exclude(pk=instance_id).exists()

        return does_with_name_exists
            
    def update_order(self, queryset_to_update, new_element_order):
        order_utils = Order()
        current_order = list(queryset_to_update.values_list('order', flat=True))
        reordered = order_utils.reorder(new_element_order, current_order)
        for index, obj in enumerate(queryset_to_update):
            obj.order = reordered[index]
            obj.save()