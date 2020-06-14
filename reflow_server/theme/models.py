from django.db import models
from reflow_server.formulary.models.abstract import AbstractField, AbstractFieldOptions, AbstractForm
from reflow_server.notification.models.abstract import AbstractNotificationConfiguration
from reflow_server.kanban.models.abstract import AbstractKanbanCard, AbstractKanbanCardField, AbstractKanbanDimensionOrder
from reflow_server.listing.models.abstract import AbstractListingTotalForField


class ThemeType(models.Model):
    """ 
    This model is a `type` so it contains required data used for this program to work. This defines the type of the
    theme. ThemeTypes are for what finality the theme was created. Could be for a Design, could be for Marketing, 
    and so on. This way it is easier to the user to travel trough the available themes.
    """
    name = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'group_type'
        ordering = ('id',)


class Theme(models.Model):
    """
    `THEMES` are called `templates` for the user, for the user they are actually the same thing. On the backend we 
    differentiate them.

    This model is actually really important. If you see the `reflow_server.formulary.models.Group` doc description
    you will probably see that groups are never created inside of reflow. This is because in order to use our app 
    the user is obligated to start selecting a Theme. 

    Themes are like a 'ctl+c / ctrl+v' of the main tables of our system, like formularies, fields and so on. When a user
    select a theme we 'copy and paste' the data from the theme tables to the ones that the user actually uses.

    It's important to know only one difference: some tables are binded to a user, on themes on the other hand they are 
    bound to a theme.
    """
    display_name = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    company_type = models.ForeignKey('theme.ThemeType', on_delete=models.CASCADE, related_name='theme_company_type', 
                                     db_index=True, null=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, related_name='theme_user', null=True)
    description = models.CharField(max_length=500, blank=True, default='')
    is_public = models.BooleanField(default=False)

    class Meta:
        db_table = 'theme'


class ThemePhotos(models.Model):
    """
    Will hold the photos to show on a carrousel of a theme. Nothing much.
    """
    theme = models.ForeignKey('theme.Theme', on_delete=models.CASCADE, db_index=True, related_name='theme_photos')
    image_name = models.CharField(max_length=300)
    url = models.CharField(max_length=1000)
    
    class Meta:
        db_table = 'theme_photos'


class ThemeForm(AbstractForm):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.formulary.models.abstract.AbstractForm` 
    and `reflow_server.formulary.models.Form` for reference
    """
    depends_on = models.ForeignKey('self', models.CASCADE, null=True, blank=True, db_index=True,
                                   related_name='depends_on_theme_form')
    form_id = models.BigIntegerField(null=True, blank=True, default=None)
    conditional_on_field = models.ForeignKey('theme.ThemeField', models.CASCADE, null=True, blank=True,
                                             related_name='conditional_on_theme_field', db_index=True)
    theme = models.ForeignKey('theme.Theme', models.CASCADE, related_name='theme_form')
    
    class Meta:
        db_table = 'theme_form'


class ThemeField(AbstractField):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.formulary.models.abstract.AbstractField` 
    and `reflow_server.formulary.models.Field` for reference
    """
    form = models.ForeignKey('theme.ThemeForm', models.CASCADE, null=True, blank=True, db_index=True,
                             related_name='theme_form_fields')
    form_field_as_option = models.ForeignKey('self', models.CASCADE, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'theme_field'


class ThemeFieldOptions(AbstractFieldOptions):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.formulary.models.abstract.AbstractFieldOptions` 
    and `reflow_server.formulary.models.FieldOptions` for reference
    """
    field = models.ForeignKey('theme.ThemeField', models.CASCADE, null=True, blank=True, db_index=True,
                              related_name='theme_field_option')

    class Meta:
        db_table = 'theme_field_options'


class ThemeListingTotalForField(AbstractListingTotalForField):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.listing.models.abstract.AbstractListingTotalForField` 
    and `reflow_server.listing.models.ListingTotalForField` for reference
    """
    field = models.ForeignKey('theme.ThemeField', models.CASCADE, db_index=True)
    theme = models.ForeignKey('theme.Theme', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'theme_listing_total_for_fields'


class ThemeKanbanCard(AbstractKanbanCard):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.kanban.models.abstract.AbstractKanbanCard` 
    and `reflow_server.kanban.models.KanbanCard` for reference
    """
    theme = models.ForeignKey('theme.Theme', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'theme_kanban_card'


class ThemeKanbanCardField(AbstractKanbanCardField):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.kanban.models.abstract.AbstractKanbanCardField` 
    and `reflow_server.kanban.models.KanbanCardField` for reference
    """
    field = models.ForeignKey('theme.ThemeField', models.CASCADE, blank=True, null=True)
    kanban_card = models.ForeignKey('theme.ThemeKanbanCard', models.CASCADE, blank=True, null=True,
                                    related_name='theme_kanban_card_fields',  db_index=True)

    class Meta:
        db_table = 'theme_kanban_card_field'


class ThemeKanbanDimensionOrder(AbstractKanbanDimensionOrder):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.kanban.models.abstract.AbstractKanbanDimensionOrder` 
    and `reflow_server.kanban.models.KanbanDimensionOrder` for reference
    """
    dimension = models.ForeignKey('theme.ThemeField', models.CASCADE, blank=True, null=True)
    theme = models.ForeignKey('theme.Theme', models.CASCADE)

    class Meta:
        db_table = 'theme_kanban_dimension_order'


class ThemeNotificationConfiguration(AbstractNotificationConfiguration):
    """
    See `reflow_server.theme.models.Theme`, `reflow_server.notification.models.abstract.AbstractNotificationConfiguration` 
    and `reflow_server.notification.models.NotificationConfiguration` for reference
    """
    field = models.ForeignKey('theme.ThemeField', models.CASCADE, db_index=True)
    form = models.ForeignKey('theme.ThemeForm', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'theme_notification_configuration'


class ThemeNotificationConfigurationVariable(models.Model):
    """
    See `reflow_server.theme.models.Theme` and `reflow_server.notification.models.NotificationConfigurationVariable` 
    for reference
    """
    field = models.ForeignKey('theme.ThemeField', models.CASCADE, db_index=True)
    notification_configuration = models.ForeignKey('theme.ThemeNotificationConfiguration', models.CASCADE, db_index=True)
    order = models.IntegerField(default=1)

    class Meta:
        db_table = 'theme_notification_configuration_variable'
