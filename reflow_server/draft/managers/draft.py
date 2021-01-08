from django.db import models


class DraftDraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def drafts_by_company_id_and_user_id(self, company_id, user_id):
        """
        Returns a bunch of reflow_server.draft.models.Draft instances by the company_id and the user_id.

        Args:
            company_id (int): A Company instance id that represents from what company this draft is from.
            user_id (int): A UserExtended instance id that represent from what user this draft is from.

        Returns:
            django.db.models.QuerySet(reflow_server.draft.models.Draft): The queryset of Draft instances
        """
        return self.get_queryset().filter(user_id=user_id, company_id=company_id)
    
    def draft_file_by_draft_id_company_id_and_user_id(self, draft_id, company_id, user_id):
        """
        Returns a single reflow_server.draft.models.Draft instance by its id, the company_id and the user_id.
        It's important that this returns only drafts that ARE files.

        Args:
            draft_id (int): A Draft instance id that you want to retrieve
            company_id (int): A Company instance id that represents from what company this draft is from.
            user_id (int): A UserExtended instance id that represent from what user this draft is from.

        Returns:
            reflow_server.draft.models.Draft: The Draft instance
        """
        return self.drafts_by_company_id_and_user_id(company_id, user_id).filter(id=draft_id, draft_type__name='file').first()

    def create_or_update_draft(self, user_id, company_id, draft_type_id, file_size=None, value=None, draft_id=None):
        """
        Creates or updates a draft. To update a draft you must set `draft_id` parameter.

        Args:
            user_id (int): The UserExtended instance id of the user that is saving this new draft.
            company_id (int): The Company instance id of what company does this draft is from.
            draft_type_id (int): If it's only a value that is stored or if it's a file. If it's a file it's probably on s3, if it's a value
                                 it don't need to be stored outside of the database.
            file_size (int, optional): The size of the file you are storing  (if it is a file). Defaults to None.
            value (str, optional): The value you are storing. Defaults to None.
            draft_id (int, optional): If you want to update a draft you probably want to set this. Defaults to None.

        Returns:
            reflow_server.draft.models.Draft: A Draft instance that was updated or created
        """
        instance, __ = self.get_queryset().update_or_create(
            id=draft_id,
            defaults={
                'value': value,
                'draft_type_id': draft_type_id,
                'file_size': file_size,
                'user_id': user_id,
                'company_id': company_id
            }
        )
        return instance
    
    def update_file_url_by_draft_id(self, draft_id, file_url):
        """
        Updates the file_url of a draft from a draft_id.

        Args:
            draft_id (id): A Draft instance id that you want to update
            file_url (str): The url of the file you saved in s3 or any other provider.

        Returns:
            int: number of updated instances, in this case, just 1.
        """
        return self.get_queryset().filter(id=draft_id).update(file_url=file_url)