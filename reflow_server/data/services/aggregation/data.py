class AggregationData:
    def __init__(self):
        """
        This class is responsible for holding the aggregation data.
        This aggregation data is a dict where each key is a DynamicFormId, and contains another dict of keys and values
        """
        self.data_dict = dict()

    def add_key(self, key, form_data_id):
        """
        Adds a new key to to the dict, so adds a new form_data_id as key and this key containing
        another dict with `key` and `value` dicts. We need to use it this way because because of
        multi_forms, we can have multiple fields_ids. FieldIds they are not always unique for 
        each formulary data.

        Args:
            key (str): The value to use as key, this is actually the value of a single FormValue
                       instance
            form_data_id (int): The DynamicFormId that this key is from.
            
        Returns:
            dict: returns the dict created for this particular form_data_id
        """
        self.data_dict[form_data_id] = {
            'key': key,
            'value': list()
        }
        return self.data_dict[form_data_id]
    
    def add_value(self, value, form_data_id):
        if form_data_id in self.data_dict:
            # we don't count values that are empty or none
            if value in [None, '']:
                value = None
            self.data_dict[form_data_id]['value'].append(value)
            return self.data_dict[form_data_id]
        else:
            return None
    
    @property
    def form_data_ids(self):
        return self.data_dict.keys()

    @property
    def aggregated(self):
        self.aggregated_data = dict()
        for data in self.data_dict.values():
            self.aggregated_data[data['key']] = self.aggregated_data.get(data['key'], []) + data['value']
        
        return self.aggregated_data