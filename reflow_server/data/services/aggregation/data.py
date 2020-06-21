class AggregationData:
    def __init__(self):
        self.data_dict = dict()

    def add_key(self, key, form_data_id):
        self.data_dict[form_data_id] = {
            'key': key,
            'value': list()
        }
        return self.data_dict[form_data_id]
    
    def add_value(self, value, form_data_id):
        if not self.data_dict:
            raise AssertionError('You need to set the keys using `.add_key()` first.')

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