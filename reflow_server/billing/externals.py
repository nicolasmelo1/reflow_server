from reflow_server.core import externals
from reflow_server.billing.serializers import VindiClientSerializer


class VindiExternal(externals.External):
    host = 'https://sandbox-app.vindi.com.br/api/v1'
    secure = False
    basic_auth = ('knbtmIJp7smiSzQdThuAquX80aHCGDV9VO2L6_mYOuU', '')

    def create_client(self, address_street, address_number, 
                      address_zip_code, address_neighborhood, 
                      address_city, address_state, address_country, 
                      company_name, company_email, company_registry_code,
                      emails=list()):
        serializer = VindiClientSerializer()
        self.post('/customers', serializer.data)