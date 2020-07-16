from reflow_server.authentication.models import Company


class VindiService:
    def __init__(self, company_id):
        self.company = Company.objects.filter(id=company_id).first()
        self.vindi_plan_id = self.company.vindi_plan_id
        self.vindi_client_id = self.company.vindi_client_id
        self.vindi_product_id = self.company.vindi_product_id
        self.vindi_payment_profile_id = self.company.vindi_payment_profile_id
        self.vindi_signature_id = self.company.vindi_signature_id

    def update_company(self):
        pass