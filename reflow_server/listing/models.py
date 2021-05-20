from django.db import models

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
