from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects
from reflow_server.formula.utils.helpers import Conversor
from reflow_server.formula.externals import GoogleSheetsExternal
from reflow_server.integration.services import IntegrationService

import json


class GoogleSheets(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def list_sheets(**kwargs):
        settings = kwargs['__settings__']
        google_sheets_external = GoogleSheetsExternal()
        integration_service = IntegrationService(settings.reflow_user_id)
        integration_authentication_data = integration_service.retrieve_integration_for_company(
            'google_sheets',
            settings.reflow_company_id
        )
        integration_authentication_data = integration_service.refresh_google_authentication_if_expired(
            integration_authentication_data
        )
        if integration_authentication_data is None:
            settings.integration_callback('google_sheets')
        else:
            conversor = Conversor(settings)
            response = google_sheets_external.all_sheets(integration_authentication_data.access_token)
            if response.status_code == 200:
                response_data = response.json()
                if 'files' in response_data:
                    files = [[drive_file['id'], drive_file['name']] for drive_file in response_data['files']]
                    return conversor.python_value_to_flow_object(files)
        
        return conversor.python_value_to_flow_object([])
    
    def _documentation_(self):
        return {
            'description': 'This library is used to interact with Google Sheets.',
            'methods': {
                'list_sheets': {
                    'description': 'Returns a list of all the sheets in your Google Drive account.',
                }
            }
        }