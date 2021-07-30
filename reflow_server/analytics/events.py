class AnalyticsEvents:
    def formulary_data_created(self, user_id, company_id, form_id, form_data_id):
        print('formulary_data_created')

    def formulary_data_updated(self, user_id, company_id, form_id, form_data_id):
        print('formulary_data_updated')
    
    def formulary_created(self, user_id, company_id, form_id):
        print('formulary_created')
    
    def formulary_updated(self, user_id, company_id, form_id):
        print('formulary_updated')

    def field_created(self, user_id, company_id, form_id, section_id, field_id):
        print('field_created')

    def field_updated(self, user_id, company_id, form_id, section_id, field_id):
        print('field_updated')