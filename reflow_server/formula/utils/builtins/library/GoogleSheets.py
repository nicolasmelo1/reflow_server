from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule


from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

import requests


class GoogleSheets(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def authorize(**kwargs):
        
        response = requests.get('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=63386062001-id1pq8bk96mo43fkg4r0e2n12ebi2mnu.apps.googleusercontent.com&redirect_uri=https://app-beta.reflow.com.br&scope=https://www.googleapis.com/auth/spreadsheets&access_type=offline&include_granted_scopes=true')
        print(response.history)
        if len(response.history) > 0:
            response = response.history[0]
            print(response.url)