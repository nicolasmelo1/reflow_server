import uuid


class FieldOptionsData:
    # ------------------------------------------------------------------------------------------
    class FieldOptionData:
        def __init__(self, option, field_option_uuid=uuid.uuid4(), field_option_id=None):
            self.field_option_uuid = str(field_option_uuid)
            self.field_option_id = field_option_id
            self.option = option
    # ------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Used for holding all of the options of the FieldOptions so we don't need to use a serializer to work with the data.
        This holds another class which is each FieldOptionData. We use a class inside a class here because we don't need
        `FieldOptionData` in any use case outside of `FieldOptionsData` class. You can read more here for reference:
        https://www.datacamp.com/community/tutorials/inner-classes-python
        """
        self.field_options = []
        self.field_options_uuids = []
        self.field_options_ids = []
    # ------------------------------------------------------------------------------------------
    def add_field_option(self, option, field_option_uuid=None, field_option_id=None):
        field_option_uuid = str(field_option_uuid) if field_option_uuid else str(uuid.uuid4())
        if field_option_uuid not in self.field_options_uuids:
            field_option_data = self.FieldOptionData(option, field_option_uuid, field_option_id)
            self.field_options.append(field_option_data)
            self.field_options_ids.append(field_option_id)
            self.field_options_uuids.append(field_option_uuid)

            return field_option_data
        return None