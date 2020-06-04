from django.db import models


class AbstractListingTotalForField(models.Model):
    # TODO: move this to dashboard. this is deprecated.
    """
    Might be moved to Dashboard, right now this holds all of the totals of the field. The Listing here means it is
    only available on `listing` visualization type
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        app_label = 'listing'
