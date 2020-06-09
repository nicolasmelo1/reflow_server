from reflow_server.core.utils import replace_dumb_characters_from_str
from reflow_server.formulary.models import Field, Form

import unicodedata
import string
import random
import re


class Order:
    """
    helper to reorder the items in the database. This adds space so you can add your order to your objects.

    Example: 
    You have 3 forms:

    - Administração - order 1
    - Negocios - order 2
    - Comercial - order 3

    Then you want to add a new one in order 2, that is already occupied by `Negocios`.
    When you use the `.order()` method you recieve a tuple like the following (2, [1,3,4])
    That means that you have the following order now:
    - Administração - order 1
    - Negocios - order 3
    - Comercial - order 4

    Leaving room to your element being inserted AFTER `Administração`, so in position 2.

    Methods:
        - `.update()` - updates the order of your queryset
    """
    def __init__(self):
        self.insert = 1

    
    def _get_next_indexes(self, current_index, element_to_check, modified_list):
        for index in range(len(modified_list)):
            if modified_list[index] == element_to_check and index != current_index:
                yield index

    def _reorder(self, number_to_add):
        # checks if the order is less than 0 (your element can't have order 0, -1 and so on). And checks if element order is above
        # the length of orders, if you have 3 elements, and want to add in position 5 you can't, the maximum position you can insert
        # is postion 4
        number_to_add = number_to_add if number_to_add > 0 else 1
        number_to_add = number_to_add if number_to_add < len(self.current_order)+1 else len(self.current_order)+1

        array = [index+1 for index in range(len(self.current_order))]

        # this might be a little confusing on start but it makes a lot of sense, next_element_indexes is an array containing all
        # the index that needs to be updated, so, if the `number_to_add` is 2 and the `self.current_order` is [1,2,3,4]
        # we first get the next_element_indexes, in this case [1], it means we must update the `self.current_order` array at index 1
        # if you want to insert the number 2 look at the index in the array.
        # `last_element` holds the number we want to add in this position. In this example, before the while it is 2, inside of the while
        # `last_element` becomes `last_element` + 1, so, number 3.
        # it's important to notice this function also works for reapeated lists or unordered lists
        next_element_indexes = list(self._get_next_indexes(None, number_to_add, array))
        last_element = number_to_add
        while next_element_indexes:
            indexes_to_check = list()
            for next_element_index in next_element_indexes:
                last_element = last_element + self.insert
                indexes_to_check = indexes_to_check + list(self._get_next_indexes(next_element_index, last_element, array))
                array[next_element_index] = last_element
            next_element_indexes = indexes_to_check
        return array
    
    def update_order(self, queryset_to_update, new_element_order):
        self.current_order = list(queryset_to_update.values_list('order', flat=True))
        reordered = self._reorder(new_element_order)
        for index, obj in enumerate(queryset_to_update):
            obj.order = reordered[index]
            obj.save()


class Settings(Order):
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
        if new_name in old_name:
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
                does_with_name_exists = Form.objects.filter(group__company_id=self.company_id, form_name=new_name).exclude(pk=instance_id).exists()
            else:
                does_with_name_exists = Field.objects.filter(form__depends_on__group__company_id=self.company_id, name=new_name).exclude(pk=instance_id).exists()

            return does_with_name_exists
            
