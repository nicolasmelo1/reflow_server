from reflow_server.core.utils import replace_dumb_characters_from_str
from reflow_server.formulary.utils.order import Order
from reflow_server.formulary.models import Field, Form

import unicodedata
import string
import random
import re


class Settings:
    def __init__(self, company_id):
        """
        This holds some handy methods that are used by Form, Field, and also Group creation.

        Args:
            company_id (int): The instance of the company that is editing the data.
        """
        self.company_id = company_id
        self.insert = 1
    
    def format_name(self, form_or_field, instance_id, old_name, label_name):
        """
        Every field or form saved have also a unique name bound to it, this name is usually unique for each company.
        This means it is not unique for every company in entire system. The idea behind names is give to users a simple
        interface to work with their data. Also this way programers can have a better way to work with 
        formularies without working directly with ids. 

        When the user edits a new notification for example, the placeholder on the text will be this name created.

        Args:
            form_or_field (tuple('form', 'field')): It's a placeholder so we know if you are trying to create a name
            for a new Form instance or a Field instance.
            instance_id (int): Can be the id of a Field intance or of a Form instance.
            old_name (str): The old name of this instance, this way if the user changes the label_name we know if we need to change
            or not.
            label_name (str): Field and Form names are created based on the label_name, the user cannot edit field_names, he can only
            edit label_names, field_names are created and generated automatically.

        Raises:
            KeyError: if the `form_or_field parameter is not `form` or `field`

        Returns:
            str: returns the newly generated name for this Field or Form.
        """
        if form_or_field not in ['form', 'field']:
            raise KeyError('`form_or_field` parameter must be a string with one of the following options: `form`, `field`')

        new_name = replace_dumb_characters_from_str(
                        unicodedata.normalize('NFKD', label_name.lower().replace(' ', '_'))
                            .encode('ascii', 'ignore').decode('utf-8').translate(
                        str.maketrans('', '', string.punctuation))
                    )
       
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
        """
        Updates the `order` of attribute of many instances of a queryset. 
        The queryset is a django.db.QuerySet object from any instances that have the `order` field in it.

        Args:
            queryset_to_update (django.db.QuerySet): This is a QuerySet object from
            `reflow_server.formulary.models.Form`, `reflow_server.formulary.models.Field` or `reflow_server.formulary.models.Group`
            models.
            new_element_order (int): The order of the new element you are trying to insert in the list.
        """
        order_utils = Order()
        # the queryset can be unorderd, here we order by the accending order or `order`
        current_order = list(queryset_to_update.values_list('order', flat=True).order_by('order'))
        reordered = order_utils.reorder(new_element_order, current_order)
        for index, obj in enumerate(queryset_to_update):
            obj.order = reordered[index]
            obj.save()