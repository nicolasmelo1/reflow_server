from django.db import models
from reflow_server.listing.models.abstract import AbstractListingTotalForField


class ListingSelectedFields(models.Model):
    """
    This is kinda dumb, but it just holds which of the fields needs to be visible in the listing table.
    If the user unselects a field, the column of the table is hidden for the user. If it is displayed, 
    the column is displayed. 
    
    Unlike kanban card fields this doesn't filter the data, that is loaded on the front end. Because on Kanban
    when the user selects another Kanban Card all of the columns go back to page 1. On listing when the user selects
    a new field to display on the column, the pagination doesn't change. 
    """
    is_selected = models.BooleanField(default=True)
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'listing_selected_fields'
        app_label = 'listing'

class ExtractFileData(models.Model):
    """
    This model is used to extract a data to the user. This works on the following architecture:

    First we send a request to the worker, then the worker request all of the data that the user is requesting.
    Since this takes too long, the request for the data is async, when it is ready we send a post request with the data to the worker
    again.
    The worker then uses this data to build a csv, the csv is then encoded as base64 and is sent back to this application
    we save the file as a base64 string in our database. Then when the user wants to download we convert the base64 csv to
    the desired user format (xlsx or csv)
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.TextField()
    file_format = models.CharField(max_length=10, default='csv')
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, db_index=True)
    form = models.ForeignKey('formulary.Form', on_delete=models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, db_index=True)

    class Meta:
        db_table = 'extract_file_data'
        app_label = 'listing'


class ListingTotalForField(AbstractListingTotalForField):
    # TODO: move this to dashboard. this is deprecated.
    # might be deleted later , it will be defined on Dashboard tables
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    number_configuration_number_format_type = models.ForeignKey('formulary.FieldNumberFormatType', on_delete=models.CASCADE, db_index=True, default=1)

    class Meta:
        db_table = 'listing_total_for_fields'
        app_label = 'listing'