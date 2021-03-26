from django.db import models


class DraftFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def draft_by_draft_id_user_id_and_company_id(self, draft_id, user_id, company_id):
        """
        Gets a single Draft instance by its id, the user it is appended to and the company it is appended to.

        Args:
            draft_id (int): A Draft instance id.
            user_id (int): A UserExtended instance id
            company_id (int): A Company instance id

        Returns:
            reflow_server.draft.models.Draft: Returns a single Draft instance based on the parameters sent.
        """
        return self.get_queryset().filter(id=draft_id, user_id=user_id, company_id=company_id).first() 
    