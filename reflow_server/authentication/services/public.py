from reflow_server.authentication.models import PublicAccess


class PublicAccessService:
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id

    def update(self):
        return PublicAccess.authentication_.update_or_create(self.user_id, self.company_id)